from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.recruiter import RecruiterCreate, RecruiterUpdate, RecruiterResponse
from app.services.recruiter_service import (
    create_recruiter,
    get_recruiter,
    get_recruiter_by_user_id,
    update_recruiter,
    delete_recruiter
)
from app.core.auth import get_current_user
from app.models.user import UserType, User

router = APIRouter(prefix="/api/v1/recruiters", tags=["recruiters"])

@router.post("/", response_model=RecruiterResponse, status_code=status.HTTP_201_CREATED)
def create_recruiter_profile(
    recruiter: RecruiterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.typeUser != UserType.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can create recruiter profiles"
        )
    
    try:
        return create_recruiter(db, current_user.id, recruiter)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=RecruiterResponse)
def get_my_recruiter_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.typeUser != UserType.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can view recruiter profiles"
        )
    
    return get_recruiter_by_user_id(db, current_user.id)

@router.get("/{recruiter_id}", response_model=RecruiterResponse)
def get_recruiter_profile(recruiter_id: int, db: Session = Depends(get_db)):
    return get_recruiter(db, recruiter_id)

@router.put("/{recruiter_id}", response_model=RecruiterResponse)
def update_recruiter_profile(
    recruiter_id: int,
    recruiter: RecruiterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.typeUser != UserType.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can update recruiter profiles"
        )
    
    return update_recruiter(db, recruiter_id, recruiter, current_user.id)

@router.delete("/{recruiter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recruiter_profile(
    recruiter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.typeUser != UserType.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can delete recruiter profiles"
        )
    
    delete_recruiter(db, recruiter_id, current_user.id) 