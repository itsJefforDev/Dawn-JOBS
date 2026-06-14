from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.job import JobResponse
from app.services.job_service import search_jobs, get_all_jobs

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

FAKE_USER_ID = 1


@router.get("/search", response_model=list[JobResponse])
def search(db: Session = Depends(get_db)):
    return search_jobs(db, FAKE_USER_ID)


@router.get("/", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return get_all_jobs(db)