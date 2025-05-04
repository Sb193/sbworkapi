from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.services.profile_service import (
    get_profile,
    get_profile_by_user_id,
    get_profiles,
    create_profile,
    update_profile,
    delete_profile
)
from app.core.auth import get_current_user, get_current_active_admin
from app.models.user import User

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])

@router.get("/", response_model=List[ProfileResponse])
def get_profiles_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    email: str = Query(None),
    full_name: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    return get_profiles(db, skip=skip, limit=limit, email=email, full_name=full_name)

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile_endpoint(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    return get_profile(db, profile_id)

@router.get("/me", response_model=ProfileResponse)
def get_my_profile_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_profile_by_user_id(db, current_user.id)

@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile_endpoint(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_profile(db, profile, current_user.id)

@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile_endpoint(
    profile_id: int,
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    return update_profile(db, profile_id, profile)

@router.put("/me", response_model=ProfileResponse)
def update_my_profile_endpoint(
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    my_profile = get_profile_by_user_id(db, current_user.id)
    return update_profile(db, my_profile.id, profile)

@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_endpoint(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    delete_profile(db, profile_id) 