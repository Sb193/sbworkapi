from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ProfileBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: Optional[List[str]] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: Optional[List[str]] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 