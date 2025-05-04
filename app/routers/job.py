from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.schemas.job_search import JobSearchQuery, JobSearchResponse
from app.services.job_service import (
    create_job,
    get_jobs,
    get_job,
    update_job,
    delete_job,
    search_jobs
)
from app.core.auth import get_current_user
from app.models.user import User, UserType
from app.models.recruiter import Recruiter

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job_endpoint(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.typeUser == UserType.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can create jobs"
        )
    
    # Get recruiter profile
    recruiter = db.query(Recruiter).filter(Recruiter.user_id == current_user.id).first()
    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found"
        )
    
    return await create_job(db, job, recruiter.id)

@router.get("/", response_model=List[JobResponse])
async def get_jobs_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_jobs(db, skip=skip, limit=limit)

@router.get("/search", response_model=JobSearchResponse)
async def search_jobs_endpoint(
    q: Optional[str] = None,
    location_id: Optional[int] = None,
    work_type_id: Optional[int] = None,
    experience_level: Optional[str] = None,
    industry: Optional[str] = None,
    tag_ids: Optional[List[int]] = None,
    salary_min: Optional[float] = None,
    salary_max: Optional[float] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    sort: str = Query("created_at", regex="^(created_at|salary_min|salary_max)$"),
    order: str = Query("desc", regex="^(asc|desc)$")
):
    query = JobSearchQuery(
        q=q,
        location_id=location_id,
        work_type_id=work_type_id,
        experience_level=experience_level,
        industry=industry,
        tag_ids=tag_ids,
        salary_min=salary_min,
        salary_max=salary_max,
        page=page,
        per_page=per_page,
        sort=sort,
        order=order
    )
    return await search_jobs(query)

@router.get("/{job_id}", response_model=JobResponse)
async def get_job_endpoint(job_id: int, db: Session = Depends(get_db)):
    job = await get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=JobResponse)
async def update_job_endpoint(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_recruiter:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can update jobs"
        )
    return await update_job(db, job_id, job, current_user.recruiter_id)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_endpoint(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_recruiter:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can delete jobs"
        )
    await delete_job(db, job_id, current_user.recruiter_id) 