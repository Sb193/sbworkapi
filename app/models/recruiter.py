from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class CompanySize(enum.Enum):
    SIZE_1_9 = "1-9"
    SIZE_10_49 = "10-49"
    SIZE_50_99 = "50-99"
    SIZE_100_499 = "100-499"
    SIZE_500_PLUS = "500+"

class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    logo_url = Column(Text)
    background_url = Column(Text)
    website = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    description = Column(Text)
    address = Column(Text)
    location = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))
    company_size = Column(Enum("1-9", "10-49", "50-99", "100-499", "500+", name="company_size"))
    founded_year = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="recruiter")
    jobs = relationship("Job", back_populates="recruiter") 