from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserType

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    typeUser: UserType = UserType.CANDIDATE

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    status: bool
    createdAt: datetime
    updateAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginResponse(BaseModel):
    user: UserResponse
    token: Token

class RegisterResponse(BaseModel):
    user: UserResponse
    token: Token

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    typeUser: Optional[UserType] = None
    status: Optional[bool] = None
