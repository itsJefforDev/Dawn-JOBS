from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.job_service import (
    search_jobs,
    get_mock_jobs,
    get_saved_jobs,
    get_unmatched_jobs
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# Trae todos los mocks sin guardar
@router.get("/all")
def all_jobs():
    return get_mock_jobs()


# Busca y guarda matches
@router.post("/search/{user_id}")
def match_jobs(user_id: int, db: Session = Depends(get_db)):
    return search_jobs(db, user_id)


# Trae historial guardado
@router.get("/history")
def job_history(db: Session = Depends(get_db)):
    return get_saved_jobs(db)

@router.get("/unmatched/{user_id}")
def unmatched_jobs(user_id: int, db: Session = Depends(get_db)):
    return get_unmatched_jobs(db, user_id)