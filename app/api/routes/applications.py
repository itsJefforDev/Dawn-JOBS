from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate
)
from app.services.application_service import (
    create_application,
    get_user_applications,
    get_application,
    update_application,
    delete_application
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/")
def save_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    return create_application(db, application)


@router.get("/{user_id}")
def list_user_applications(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_applications(db, user_id)


@router.put("/{application_id}")
def update_application_status(
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    updated = update_application(db, application_id, data)

    if not updated:
        raise HTTPException(404, "Application not found")

    return updated


@router.delete("/{application_id}")
def remove_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_application(db, application_id)

    if not deleted:
        raise HTTPException(404, "Application not found")

    return deleted