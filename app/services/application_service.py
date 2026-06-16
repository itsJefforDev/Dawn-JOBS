from sqlalchemy.orm import Session
from app.models.application import Application


def create_application(db: Session, application_data):
    application = Application(**application_data.dict())

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_user_applications(db: Session, user_id: int):
    return db.query(Application).filter(
        Application.user_id == user_id
    ).all()


def get_application(db: Session, application_id: int):
    return db.query(Application).filter(
        Application.id == application_id
    ).first()


def update_application(db: Session, application_id: int, data):
    application = get_application(db, application_id)

    if not application:
        return None

    application.status = data.status
    application.notes = data.notes

    db.commit()
    db.refresh(application)

    return application


def delete_application(db: Session, application_id: int):
    application = get_application(db, application_id)

    if not application:
        return None

    db.delete(application)
    db.commit()

    return {"message": "Application deleted"}