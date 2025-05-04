from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserResponse, UserUpdate, ChangePassword
from app.core.security import get_password_hash, verify_password
from typing import List, Optional

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    email: Optional[str] = None,
    type_user: Optional[UserType] = None,
    is_active: Optional[bool] = None
) -> List[User]:
    query = db.query(User)
    
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if type_user:
        query = query.filter(User.typeUser == type_user)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    # Check if user already exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = User(
        email=user.email,
        fullName=user.fullName,
        typeUser=user.typeUser,
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    db_user = get_user_by_id(db, user_id)
    
    # Check if new email is already taken
    if user.email and user.email != db_user.email:
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update user fields
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()

def change_password(db: Session, user_id: int, password_data: ChangePassword) -> User:
    user = get_user_by_id(db, user_id)
    
    # Verify current password
    if not verify_password(password_data.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Verify new password and confirm password match
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match"
        )
    
    # Update password
    user.password = get_password_hash(password_data.new_password)
    db.commit()
    db.refresh(user)
    
    return user 