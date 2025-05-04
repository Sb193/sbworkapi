from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse

def get_profile(db: Session, profile_id: int) -> Profile:
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

def get_profile_by_user_id(db: Session, user_id: int) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

def get_profiles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    email: Optional[str] = None,
    full_name: Optional[str] = None
) -> List[Profile]:
    query = db.query(Profile)
    
    if email:
        query = query.filter(Profile.email.ilike(f"%{email}%"))
    if full_name:
        query = query.filter(Profile.full_name.ilike(f"%{full_name}%"))
    
    return query.offset(skip).limit(limit).all()

def create_profile(db: Session, profile: ProfileCreate, user_id: int) -> Profile:
    # Check if user already has a profile
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a profile"
        )
    
    # Check if email is already taken
    existing_email = db.query(Profile).filter(Profile.email == profile.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_profile = Profile(
        user_id=user_id,
        full_name=profile.full_name,
        email=profile.email,
        phone=profile.phone,
        address=profile.address,
        skills=profile.skills
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: int, profile: ProfileUpdate) -> Profile:
    db_profile = get_profile(db, profile_id)
    
    # Check if new email is already taken
    if profile.email and profile.email != db_profile.email:
        existing_email = db.query(Profile).filter(Profile.email == profile.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update profile fields
    update_data = profile.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    db_profile = get_profile(db, profile_id)
    db.delete(db_profile)
    db.commit() 