import asyncio
import random
from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.job_preference import JobPreference
from app.models.auto_apply import AutoApplyLog
from app.models.application import Application


async def auto_apply_jobs(db: Session, user_id: int):
    preference = db.query(JobPreference).filter(
        JobPreference.user_id == user_id
    ).first()

    if not preference:
        return {"message": "No preferences found"}

    jobs = db.query(Job).filter(
        Job.title.ilike(f"%{preference.role}%")
    ).all()

    if preference.modality:
        jobs = [
            job for job in jobs
            if job.modality == preference.modality
        ]

    results = []

    for job in jobs:
        already_applied = db.query(Application).filter(
            Application.user_id == user_id,
            Application.job_id == job.id
        ).first()

        if already_applied:
            log = AutoApplyLog(
                user_id=user_id,
                job_id=job.id,
                status="skipped",
                message="Already applied"
            )

        else:
            # Delay aleatorio para simular comportamiento humano
            delay = random.randint(5, 15)
            await asyncio.sleep(delay)


            application = Application(
                user_id=user_id,
                job_id=job.id,
                status="applied",
                notes="AutoApply"
            )

            db.add(application)

            log = AutoApplyLog(
                user_id=user_id,
                job_id=job.id,
                status="success",
                message=f"Application sent successfully after {delay}s"
            )

        db.add(log)

        # Un solo commit por ciclo
        db.commit()

        db.refresh(log)

        results.append({
            "id": log.id,
            "user_id": log.user_id,
            "job_id": log.job_id,
            "status": log.status,
            "message": log.message,
            "created_at": log.created_at
        })

    return results