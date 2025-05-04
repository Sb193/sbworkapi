from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "SBWork API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DB_HOST: str = os.getenv("DB_HOST", "mysql-container")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "Sbac@19032003")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "sbworkdb")
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis-server")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    REDIS_DB: int = 0
    
    # MinIO settings
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "minio-server")
    MINIO_PORT: str = os.getenv("MINIO_PORT", "9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "DDqHhYEKcLHdC6Y2Y4aV")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "wk1rd9ohZq9aghNmowPHTpN6VFjCSA6XrubS8W7H")
    
    # Elasticsearch settings
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    ELASTICSEARCH_PORT: int = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    ELASTICSEARCH_URL: str = f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    @property
    def DATABASE_URL(self) -> str:
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASSWORD)
        host = self.DB_HOST
        port = self.DB_PORT
        database = self.DB_DATABASE
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def MINIO_URL(self) -> str:
        return f"http://{self.MINIO_ENDPOINT}:{self.MINIO_PORT}"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
