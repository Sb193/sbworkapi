from datetime import timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, get_current_user_token
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserLogin, Token, LoginResponse, UserResponse, RegisterResponse
from app.db.redis_db import get_redis
from app.db.database import get_db

redis_client = get_redis()

def register_user(db: Session, user: UserCreate) -> RegisterResponse:
    # Prevent admin user registration
    if user.typeUser == UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot register admin user"
        )
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        name=user.name,
        password=hashed_password,
        typeUser=user.typeUser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    
    # Store tokens in Redis
    redis_client.set(f"access_token:{db_user.username}", access_token)
    redis_client.set(f"refresh_token:{db_user.username}", refresh_token)
    
    # Create user response
    user_response = UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        name=db_user.name,
        typeUser=db_user.typeUser,
        status=db_user.status,
        createdAt=db_user.createdAt,
        updateAt=db_user.updateAt
    )
    
    # Create token response
    token_response = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
    
    return RegisterResponse(
        user=user_response,
        token=token_response
    )

def login_user(db: Session, user: UserLogin) -> LoginResponse:
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not db_user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    
    # Store tokens in Redis
    redis_client.set(f"access_token:{db_user.username}", access_token)
    redis_client.set(f"refresh_token:{db_user.username}", refresh_token)
    
    # Create user response
    user_response = UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        name=db_user.name,
        typeUser=db_user.typeUser,
        status=db_user.status,
        createdAt=db_user.createdAt,
        updateAt=db_user.updateAt
    )
    
    # Create token response
    token_response = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
    
    return LoginResponse(
        user=user_response,
        token=token_response
    )

def logout_user(username: str):
    # Remove tokens from Redis
    redis_client.delete(f"access_token:{username}")
    redis_client.delete(f"refresh_token:{username}")

def verify_token_in_redis(username: str, token: str) -> bool:
    stored_token = redis_client.get(f"access_token:{username}")
    return stored_token == token if stored_token else False

def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_current_user_token)) -> User:
    username = token.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    
    return user
