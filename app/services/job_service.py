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


# Devuelve TODOS los mocks sin guardar nada
def get_mock_jobs():
    return MOCK_JOBS


# Busca según preferencias y guarda solo matches
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
            # Evita duplicados
            existing_job = db.query(Job).filter(
                Job.url == job_data["url"]
            ).first()

            if not existing_job:
                job = Job(**job_data)
                db.add(job)
                db.commit()
                db.refresh(job)
                matched_jobs.append(job)
            else:
                matched_jobs.append(existing_job)

    return matched_jobs


# Historial guardado
def get_saved_jobs(db: Session):
    return db.query(Job).all()
