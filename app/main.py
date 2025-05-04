from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import  user, recruiter, job, auth
from app.db.database import engine
from app.models import user as user_model, job as job_model
from app.core.config import settings
from app.core.elasticsearch import init_elasticsearch, close_elasticsearch
import uvicorn

user_model.Base.metadata.create_all(bind=engine)
job_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(recruiter.router)
app.include_router(job.router)

@app.on_event("startup")
async def startup_event():
    await init_elasticsearch()

@app.on_event("shutdown")
async def shutdown_event():
    await close_elasticsearch()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
