"""
Rutas del módulo Applications.

Todas las operaciones requieren autenticación mediante JWT.

El usuario autenticado se obtiene automáticamente mediante
la dependencia get_current_user().

Nunca se recibe user_id desde el frontend.

Endpoints
---------
POST    /applications            Crear una postulación
GET     /applications/me         Obtener mis postulaciones
PUT     /applications/{id}       Actualizar una postulación
DELETE  /applications/{id}       Eliminar una postulación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse
)

from app.services.application_service import (
    create_application,
    get_application,
    update_application,
    delete_application
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# ==========================================================
# CREATE APPLICATION
# ==========================================================

@router.post(
    "/",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Guardar una postulación",
    description="""
Guarda una nueva postulación del usuario autenticado.

El usuario se obtiene automáticamente desde el JWT.
"""
)
def save_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_application(
        db,
        current_user,
        application
    )


# ==========================================================
# GET MY APPLICATIONS
# ==========================================================

@router.get(
    "/me",
    response_model=list[ApplicationResponse],
    summary="Obtener mis postulaciones",
    description="""
Devuelve todas las postulaciones realizadas por el
usuario autenticado.
"""
)
def list_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_my_applications(
        db,
        current_user
    )


# ==========================================================
# UPDATE APPLICATION
# ==========================================================

@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Actualizar una postulación",
    description="""
Actualiza el estado de una postulación.

La postulación debe pertenecer al usuario autenticado.
"""
)
def update_application_status(
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    updated = update_application(
        db,
        current_user,
        application_id,
        data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found."
        )

    return updated


# ==========================================================
# DELETE APPLICATION
# ==========================================================

@router.delete(
    "/{application_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar una postulación",
    description="""
Elimina una postulación.

Sólo puede eliminarse si pertenece al usuario autenticado.
"""
)
def remove_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    deleted = delete_application(
        db,
        current_user,
        application_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found."
        )

    return {
        "message": "Application deleted successfully."
    }