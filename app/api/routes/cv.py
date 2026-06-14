from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cv import CVResponse
from app.services.cv_service import save_cv, get_cv, delete_cv

router = APIRouter(
    prefix="/cv",
    tags=["CV"]
)

FAKE_USER_ID = 1


@router.post("/upload", response_model=CVResponse)
def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return save_cv(db, FAKE_USER_ID, file)


@router.get("/me", response_model=CVResponse)
def get_my_cv(db: Session = Depends(get_db)):
    return get_cv(db, FAKE_USER_ID)


@router.delete("/me")
def delete_my_cv(db: Session = Depends(get_db)):
    return delete_cv(db, FAKE_USER_ID)