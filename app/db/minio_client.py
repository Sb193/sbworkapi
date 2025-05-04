from minio import Minio
from app.core.config import settings

minio_client = Minio(
    f"{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}",
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def get_minio():
    return minio_client 