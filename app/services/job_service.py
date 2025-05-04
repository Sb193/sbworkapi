from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.job import Job, Tag, Location, WorkType
from app.models.recruiter import Recruiter
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.schemas.job_search import JobSearchQuery, JobSearchResponse
from app.db.redis_db import get_redis
from app.core.elasticsearch_manager import es_manager
import json
import hashlib

redis_client = get_redis()
REDIS_DB = 1  # Use database 1 for jobs

def get_cache_key(query: Dict[str, Any]) -> str:
    """Tạo cache key từ query parameters"""
    query_str = json.dumps(query, sort_keys=True)
    return f"job_search:{hashlib.md5(query_str.encode()).hexdigest()}"

def get_job_from_cache(job_id: int) -> Optional[JobResponse]:
    cached_job = redis_client.get(f"job:{job_id}")
    if cached_job:
        return JobResponse.model_validate_json(cached_job)
    return None

def set_job_in_cache(job: JobResponse):
    redis_client.set(f"job:{job.id}", job.model_dump_json())
    redis_client.expire(f"job:{job.id}", 3600)  # Cache for 1 hour

def invalidate_job_cache(job_id: int):
    redis_client.delete(f"job:{job_id}")

async def search_jobs(query: JobSearchQuery) -> JobSearchResponse:
    # Tạo cache key
    cache_key = get_cache_key(query.model_dump())
    
    # Kiểm tra cache
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return JobSearchResponse.model_validate_json(cached_result)
    
    # Tạo Elasticsearch query
    es_query = {
        "bool": {
            "must": [],
            "filter": []
        }
    }
    
    # Thêm full-text search
    if query.q:
        es_query["bool"]["must"].append({
            "multi_match": {
                "query": query.q,
                "fields": ["title", "description"],
                "type": "best_fields"
            }
        })
    
    # Thêm filters
    if query.location_id:
        es_query["bool"]["filter"].append({"term": {"location_id": query.location_id}})
    if query.work_type_id:
        es_query["bool"]["filter"].append({"term": {"work_type_id": query.work_type_id}})
    if query.experience_level:
        es_query["bool"]["filter"].append({"term": {"experience_level": query.experience_level}})
    if query.industry:
        es_query["bool"]["filter"].append({"term": {"industry": query.industry}})
    if query.tag_ids:
        es_query["bool"]["filter"].append({"terms": {"tags": query.tag_ids}})
    if query.salary_min is not None:
        es_query["bool"]["filter"].append({"range": {"salary_min": {"gte": query.salary_min}}})
    if query.salary_max is not None:
        es_query["bool"]["filter"].append({"range": {"salary_max": {"lte": query.salary_max}}})
    
    # Thực hiện tìm kiếm
    result = await es_manager.search(
        index_name="jobs",
        query=es_query,
        from_=(query.page - 1) * query.per_page,
        size=query.per_page,
        sort={query.sort: {"order": query.order}}
    )
    
    # Tạo response
    total = result["hits"]["total"]["value"]
    items = [hit["_source"] for hit in result["hits"]["hits"]]
    
    response = JobSearchResponse(
        items=items,
        total=total,
        page=query.page,
        per_page=query.per_page,
        total_pages=(total + query.per_page - 1) // query.per_page
    )
    
    # Cache kết quả
    redis_client.set(cache_key, response.model_dump_json())
    redis_client.expire(cache_key, 3600)  # Cache for 1 hour
    
    return response

async def index_job(job: Job):
    """Index job vào Elasticsearch"""
    await es_manager.index_document(
        index_name="jobs",
        document_id=job.id,
        document={
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "location_id": job.location_id,
            "work_type_id": job.work_type_id,
            "recruiter_id": job.recruiter_id,
            "experience_level": job.experience_level,
            "industry": job.industry,
            "created_at": job.created_at.isoformat(),
            "tags": [tag.id for tag in job.tags]
        }
    )

async def delete_job_from_index(job_id: int):
    """Xóa job khỏi Elasticsearch index"""
    await es_manager.delete_document(index_name="jobs", document_id=job_id)

async def create_job(db: Session, job: JobCreate, recruiter_id: int) -> JobResponse:
    # Verify recruiter exists
    recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter not found"
        )
    
    # Create job
    db_job = Job(
        title=job.title,
        description=job.description,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        location_id=job.location_id,
        work_type_id=job.work_type_id,
        recruiter_id=recruiter_id,
        experience_level=job.experience_level,
        industry=job.industry
    )
    
    # Add tags if provided
    if job.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(job.tag_ids)).all()
        db_job.tags = tags
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Index vào Elasticsearch
    await index_job(db_job)
    
    # Convert to response model
    job_response = JobResponse.model_validate(db_job)
    
    # Cache the job
    set_job_in_cache(job_response)
    
    return job_response

def get_job(db: Session, job_id: int) -> JobResponse:
    # Try to get from cache first
    cached_job = get_job_from_cache(job_id)
    if cached_job:
        return cached_job
    
    # If not in cache, get from database
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Convert to response model and cache
    job_response = JobResponse.model_validate(db_job)
    set_job_in_cache(job_response)
    
    return job_response

def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    location_id: Optional[int] = None,
    work_type_id: Optional[int] = None,
    experience_level: Optional[str] = None,
    industry: Optional[str] = None,
    tag_ids: Optional[List[int]] = None,
    recruiter_id: Optional[int] = None
) -> List[JobResponse]:
    query = db.query(Job)
    
    # Apply filters
    if location_id:
        query = query.filter(Job.location_id == location_id)
    if work_type_id:
        query = query.filter(Job.work_type_id == work_type_id)
    if experience_level:
        query = query.filter(Job.experience_level == experience_level)
    if industry:
        query = query.filter(Job.industry == industry)
    if tag_ids:
        query = query.join(Job.tags).filter(Tag.id.in_(tag_ids))
    if recruiter_id:
        query = query.filter(Job.recruiter_id == recruiter_id)
    
    # Execute query
    jobs = query.offset(skip).limit(limit).all()
    
    # Convert to response models
    return [JobResponse.model_validate(job) for job in jobs]

async def update_job(db: Session, job_id: int, job: JobUpdate, recruiter_id: int) -> JobResponse:
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if the job belongs to the recruiter
    if db_job.recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own jobs"
        )
    
    # Update fields
    update_data = job.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field != "tag_ids":
            setattr(db_job, field, value)
    
    # Update tags if provided
    if "tag_ids" in update_data:
        tags = db.query(Tag).filter(Tag.id.in_(update_data["tag_ids"])).all()
        db_job.tags = tags
    
    db.commit()
    db.refresh(db_job)
    
    # Update Elasticsearch index
    await index_job(db_job)
    
    # Update cache
    job_response = JobResponse.model_validate(db_job)
    set_job_in_cache(job_response)
    
    return job_response

async def delete_job(db: Session, job_id: int, recruiter_id: int):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if the job belongs to the recruiter
    if db_job.recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own jobs"
        )
    
    # Delete from Elasticsearch
    await delete_job_from_index(job_id)
    
    # Delete from cache
    invalidate_job_cache(job_id)
    
    db.delete(db_job)
    db.commit() 