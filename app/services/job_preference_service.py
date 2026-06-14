from sqlalchemy.orm import Session
from app.models.job_preference import JobPreference
from app.schemas.job_preference import JobPreferenceCreate, JobPreferenceUpdate


def create_preferences(db: Session, user_id: int, data: JobPreferenceCreate):
    preference = JobPreference(
        user_id=user_id,
        **data.dict()
    )

    db.add(preference)
    db.commit()
    db.refresh(preference)

    return preference


def get_preferences(db: Session, user_id: int):
    return db.query(JobPreference).filter(
        JobPreference.user_id == user_id
    ).first()


def update_preferences(db: Session, user_id: int, data: JobPreferenceUpdate):
    preference = get_preferences(db, user_id)

    if not preference:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(preference, key, value)

    db.commit()
    db.refresh(preference)

    return preference


def delete_preferences(db: Session, user_id: int):
    preference = get_preferences(db, user_id)

    if not preference:
        return None

    db.delete(preference)
    db.commit()

    return {"message": "Preferences deleted successfully"}