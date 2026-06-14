from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.job_preference import JobPreference


MOCK_JOBS = [
    {
        "title": "Backend Developer",
        "company": "TechNova",
        "location": "Colombia",
        "modality": "remote",
        "salary": 4000,
        "source": "RemoteOK",
        "url": "https://example.com/job1"
    },
    {
        "title": "Python Developer",
        "company": "DevSolutions",
        "location": "USA",
        "modality": "hybrid",
        "salary": 5000,
        "source": "Indeed",
        "url": "https://example.com/job2"
    }
]


def search_jobs(db: Session, user_id: int):
    preference = db.query(JobPreference).filter(
        JobPreference.user_id == user_id
    ).first()

    if not preference:
        return []

    matched_jobs = []

    for job_data in MOCK_JOBS:
        if (
            preference.role.lower() in job_data["title"].lower()
            and (
                preference.modality is None
                or preference.modality == job_data["modality"]
            )
        ):
            job = Job(**job_data)
            db.add(job)
            matched_jobs.append(job)

    db.commit()

    for job in matched_jobs:
        db.refresh(job)

    return matched_jobs


def get_all_jobs(db: Session):
    return db.query(Job).all()