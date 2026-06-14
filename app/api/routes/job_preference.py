from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.job_preference import (
    JobPreferenceCreate,
    JobPreferenceUpdate,
    JobPreferenceResponse
)
from app.services.job_preference_service import (
    create_preferences,
    get_preferences,
    update_preferences,
    delete_preferences
)

router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"]
)

FAKE_USER_ID = 1


@router.post("/", response_model=JobPreferenceResponse)
def create(data: JobPreferenceCreate, db: Session = Depends(get_db)):
    return create_preferences(db, FAKE_USER_ID, data)


@router.get("/me", response_model=JobPreferenceResponse)
def get_my_preferences(db: Session = Depends(get_db)):
    return get_preferences(db, FAKE_USER_ID)


@router.put("/me", response_model=JobPreferenceResponse)
def update(data: JobPreferenceUpdate, db: Session = Depends(get_db)):
    return update_preferences(db, FAKE_USER_ID, data)


@router.delete("/me")
def delete(db: Session = Depends(get_db)):
    return delete_preferences(db, FAKE_USER_ID)