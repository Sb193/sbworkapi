from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))
    work_type_id = Column(Integer, ForeignKey("work_types.id", ondelete="SET NULL"))
    recruiter_id = Column(Integer, ForeignKey("recruiters.id", ondelete="CASCADE"), nullable=False)
    experience_level = Column(Enum("Junior", "Mid", "Senior", name="experience_level"))
    industry = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    location = relationship("Location", back_populates="jobs")
    work_type = relationship("WorkType", back_populates="jobs")
    recruiter = relationship("Recruiter", back_populates="jobs")
    tags = relationship("Tag", secondary="job_tags", back_populates="jobs")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    jobs = relationship("Job", secondary="job_tags", back_populates="tags")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    
    # Relationships
    jobs = relationship("Job", back_populates="location")

class WorkType(Base):
    __tablename__ = "work_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    jobs = relationship("Job", back_populates="work_type")

# Association table for many-to-many relationship between jobs and tags
job_tags = Table(
    "job_tags",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
) 