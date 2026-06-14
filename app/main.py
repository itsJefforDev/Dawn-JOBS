from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.core.database import Base, engine
from app.api.routes.profile import router as profile_router
from app.models.profile import Profile
from app.api.routes.job_preference import router as preference_router
from app.models.job_preference import JobPreference

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Bot API"
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(preference_router)

@app.get("/")
def root():
    return {"message": "Job Bot API running"}