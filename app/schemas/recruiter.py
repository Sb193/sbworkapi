from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal
from datetime import datetime

CompanySizeType = Literal["1-9", "10-49", "50-99", "100-499", "500+"]

class RecruiterBase(BaseModel):
    name: str
    slug: str
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    location: Optional[int] = None
    company_size: Optional[CompanySizeType] = None
    founded_year: Optional[int] = None

class RecruiterCreate(RecruiterBase):
    pass

class RecruiterUpdate(RecruiterBase):
    name: Optional[str] = None
    slug: Optional[str] = None

class RecruiterResponse(RecruiterBase):
    id: int
    user_id: int
    logo_url: Optional[str] = None
    background_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 