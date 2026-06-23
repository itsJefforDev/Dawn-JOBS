from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.profile import router as profile_router
from app.api.routes.job_preference import router as preferences_router
from app.api.routes.job import router as jobs_router
from app.api.routes.cv import router as cv_router
from app.api.routes.applications import router as application_router
from app.api.routes.auto_apply import router as auto_apply_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,

    # Para desarrollo puedes usar "*"
    # allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(preferences_router)
app.include_router(jobs_router)
app.include_router(cv_router)
app.include_router(application_router)
app.include_router(auto_apply_router)