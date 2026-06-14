from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.services.profile_service import (
    create_profile,
    get_profiles,
    get_profile_by_id,
    delete_profile
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=ProfileResponse)
def create(profile: ProfileCreate, db: Session = Depends(get_db)):
    return create_profile(db, user_id=1, profile=profile)


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_profiles(db)


@router.get("/{profile_id}")
def get_one(profile_id: int, db: Session = Depends(get_db)):
    profile = get_profile_by_id(db, profile_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.delete("/{profile_id}")
def remove(profile_id: int, db: Session = Depends(get_db)):
    profile = delete_profile(db, profile_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"message": "Profile deleted successfully"}