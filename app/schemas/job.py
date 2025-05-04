from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ExperienceLevel(str, Enum):
    JUNIOR = "Junior"
    MID = "Mid"
    SENIOR = "Senior"

class JobBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location_id: Optional[int] = None
    work_type_id: Optional[int] = None
    experience_level: Optional[ExperienceLevel] = None
    industry: Optional[str] = Field(None, max_length=100)
    tag_ids: Optional[List[int]] = []

class JobCreate(JobBase):
    recruiter_id: int

class JobUpdate(JobBase):
    title: Optional[str] = Field(None, max_length=255)
    recruiter_id: Optional[int] = None

class TagBase(BaseModel):
    name: str = Field(..., max_length=50)

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int

    class Config:
        from_attributes = True

class LocationBase(BaseModel):
    name: str = Field(..., max_length=255)

class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: int

    class Config:
        from_attributes = True

class WorkTypeBase(BaseModel):
    name: str = Field(..., max_length=50)

class WorkTypeCreate(WorkTypeBase):
    pass

class WorkTypeResponse(WorkTypeBase):
    id: int

    class Config:
        from_attributes = True

class JobResponse(JobBase):
    id: int
    recruiter_id: int
    created_at: datetime
    location: Optional[LocationResponse] = None
    work_type: Optional[WorkTypeResponse] = None
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True 