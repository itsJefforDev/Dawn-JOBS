from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate
from app.schemas.profile import ProfileUpdate

def create_profile(db: Session, user_id: int, profile: ProfileCreate):
    new_profile = Profile(
        user_id=user_id,
        full_name=profile.full_name,
        title=profile.title,
        skills=profile.skills,
        experience=profile.experience,
        english_level=profile.english_level,
        location=profile.location,
        salary_expectation=profile.salary_expectation,
        work_mode=profile.work_mode
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


def get_profiles(db: Session):
    return db.query(Profile).all()


def get_profile_by_id(db: Session, profile_id: int):
    return db.query(Profile).filter(Profile.id == profile_id).first()


def delete_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        return None

    db.delete(profile)
    db.commit()

    return profile


def update_profile(db: Session, profile_id: int, profile_data: ProfileUpdate):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        return None

    update_data = profile_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return profile