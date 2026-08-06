from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate
)


# ==========================================================
# Crear una nueva postulación
# ==========================================================
def create_application(
    db: Session,
    user_id: int,
    application_data: ApplicationCreate
):
    """
    Crea una nueva postulación para el usuario autenticado.

    El user_id NO proviene del frontend.
    Se obtiene directamente del JWT.
    """

    application = Application(
        user_id=user_id,
        job_id=application_data.job_id,
        notes=application_data.notes,
        status="saved"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


# ==========================================================
# Obtener todas las postulaciones del usuario autenticado
# ==========================================================
def get_user_applications(
    db: Session,
    user_id: int
):
    """
    Devuelve únicamente las postulaciones
    pertenecientes al usuario autenticado.
    """

    return (
        db.query(Application)
        .filter(Application.user_id == user_id)
        .all()
    )


# ==========================================================
# Obtener una postulación específica
# ==========================================================
def get_application(
    db: Session,
    application_id: int,
    user_id: int
):
    """
    Busca una postulación únicamente si
    pertenece al usuario autenticado.

    Esto evita que un usuario pueda consultar
    postulaciones de otra persona modificando
    el ID en la URL.
    """

    return (
        db.query(Application)
        .filter(
            Application.id == application_id,
            Application.user_id == user_id
        )
        .first()
    )


# ==========================================================
# Actualizar una postulación
# ==========================================================
def update_application(
    db: Session,
    application_id: int,
    user_id: int,
    data: ApplicationUpdate
):
    """
    Actualiza únicamente una postulación
    perteneciente al usuario autenticado.
    """

    application = get_application(
        db,
        application_id,
        user_id
    )

    if not application:
        return None

    # Solo actualizamos los campos enviados
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)

    return application


# ==========================================================
# Eliminar una postulación
# ==========================================================
def delete_application(
    db: Session,
    application_id: int,
    user_id: int
):
    """
    Elimina únicamente una postulación
    perteneciente al usuario autenticado.
    """

    application = get_application(
        db,
        application_id,
        user_id
    )

    if not application:
        return None

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }