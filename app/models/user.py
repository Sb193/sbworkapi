from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class UserType(enum.Enum):
    ADMIN = 1
    CANDIDATE = 2
    RECRUITER = 3

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    typeUser = Column(Enum(UserType), default=UserType.CANDIDATE, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updateAt = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    recruiter = relationship("Recruiter", back_populates="user", uselist=False)
