from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.core.database import Base, engine
from app.api.routes.profile import router as profile_router
from app.models.profile import Profile
from app.api.routes.job_preference import router as preference_router
from app.models.job_preference import JobPreference
from app.api.routes.cv import router as cv_router
from app.models.cv import CV
from app.api.routes.job import router as job_router
from app.models.job import Job
from app.api.routes.applications import router as application_router
from app.api.routes.auto_apply import router as auto_apply_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Bot API"
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(preference_router)
app.include_router(cv_router)
app.include_router(job_router)
app.include_router(application_router)
app.include_router(auto_apply_router)

@app.get("/")
def root():
    return {"message": "Job Bot API running"}