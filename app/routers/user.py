from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, LoginResponse, RegisterResponse, UserUpdate
from app.services.auth_service import register_user, login_user, logout_user, verify_token_in_redis
from app.core.security import verify_token
from app.models.user import User, UserType
from app.services.user_service import (
    get_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)
from app.core.auth import get_current_user, get_current_active_admin

router = APIRouter(prefix="/api/v1/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    if not verify_token_in_redis(username, token):
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user



@router.get("/", response_model=List[UserResponse])
def get_users_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    email: str = Query(None),
    type_user: UserType = Query(None),
    is_active: bool = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    return get_users(db, skip=skip, limit=limit, email=email, type_user=type_user, is_active=is_active)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    return get_user_by_id(db, user_id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    return create_user(db, user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    return update_user(db, user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    delete_user(db, user_id)

@router.put("/me", response_model=UserResponse)
def update_user_info(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_user(db, current_user.id, user)

