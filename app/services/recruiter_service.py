from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.recruiter import Recruiter
from app.schemas.recruiter import RecruiterCreate, RecruiterUpdate, RecruiterResponse
from app.db.redis_db import get_redis
import json

redis_client = get_redis()
REDIS_DB = 2  # Use database 2 for recruiters

def get_recruiter_from_cache(recruiter_id: int) -> Optional[RecruiterResponse]:
    cached_recruiter = redis_client.get(f"recruiter:{recruiter_id}")
    if cached_recruiter:
        return RecruiterResponse.model_validate_json(cached_recruiter)
    return None

def set_recruiter_in_cache(recruiter: RecruiterResponse):
    redis_client.set(f"recruiter:{recruiter.id}", recruiter.model_dump_json())
    redis_client.expire(f"recruiter:{recruiter.id}", 3600)  # Cache for 1 hour

def invalidate_recruiter_cache(recruiter_id: int):
    redis_client.delete(f"recruiter:{recruiter_id}")

def create_recruiter(db: Session, user_id: int, recruiter: RecruiterCreate) -> RecruiterResponse:
    # Check if user already has a recruiter profile
    existing_recruiter = db.query(Recruiter).filter(Recruiter.user_id == user_id).first()
    if existing_recruiter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a recruiter profile"
        )

    # Create recruiter
    db_recruiter = Recruiter(
        user_id=user_id,
        name=recruiter.name,
        slug=recruiter.slug,
        website=recruiter.website,
        email=recruiter.email,
        phone=recruiter.phone,
        description=recruiter.description,
        address=recruiter.address,
        location=recruiter.location,
        company_size=recruiter.company_size,
        founded_year=recruiter.founded_year
    )
    
    db.add(db_recruiter)
    db.commit()
    db.refresh(db_recruiter)
    
    # Convert to response model
    recruiter_response = RecruiterResponse.model_validate(db_recruiter)
    
    # Cache the recruiter
    set_recruiter_in_cache(recruiter_response)
    
    return recruiter_response

def get_recruiter(db: Session, recruiter_id: int) -> RecruiterResponse:
    # Try to get from cache first
    cached_recruiter = get_recruiter_from_cache(recruiter_id)
    if cached_recruiter:
        return cached_recruiter
    
    # If not in cache, get from database
    db_recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
    if not db_recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter not found"
        )
    
    # Convert to response model and cache
    recruiter_response = RecruiterResponse.model_validate(db_recruiter)
    set_recruiter_in_cache(recruiter_response)
    
    return recruiter_response

def get_recruiter_by_user_id(db: Session, user_id: int) -> RecruiterResponse:
    db_recruiter = db.query(Recruiter).filter(Recruiter.user_id == user_id).first()
    if not db_recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter not found"
        )
    return RecruiterResponse.model_validate(db_recruiter)

def update_recruiter(db: Session, recruiter_id: int, recruiter: RecruiterUpdate, current_user_id: int) -> RecruiterResponse:
    db_recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
    if not db_recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter not found"
        )
    
    # Check if the recruiter profile belongs to the current user
    if db_recruiter.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own recruiter profile"
        )
    
    # Update fields
    update_data = recruiter.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_recruiter, field, value)
    
    db.commit()
    db.refresh(db_recruiter)
    
    # Convert to response model and update cache
    recruiter_response = RecruiterResponse.model_validate(db_recruiter)
    set_recruiter_in_cache(recruiter_response)
    
    return recruiter_response

def delete_recruiter(db: Session, recruiter_id: int, current_user_id: int):
    db_recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
    if not db_recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter not found"
        )
    
    # Check if the recruiter profile belongs to the current user
    if db_recruiter.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own recruiter profile"
        )
    
    db.delete(db_recruiter)
    db.commit()
    
    # Invalidate cache
    invalidate_recruiter_cache(recruiter_id) 