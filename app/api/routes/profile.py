"""
Rutas del módulo Profile.

Todas las operaciones requieren autenticación mediante JWT.

El usuario autenticado es obtenido automáticamente mediante
la dependencia get_current_user(), evitando recibir user_id
desde el frontend.

Endpoints:

POST    /profile/me      Crear perfil
GET     /profile/me      Obtener mi perfil
PUT     /profile/me      Actualizar mi perfil
DELETE  /profile/me      Eliminar mi perfil
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse
)

from app.services import profile_service


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


# ==========================================================
# CREATE PROFILE
# ==========================================================

@router.post(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear mi perfil",
    description="""
Crea el perfil profesional del usuario autenticado.

Un usuario únicamente puede tener un perfil.
Si ya existe uno, se devolverá un error.
"""
)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_profile = profile_service.create_profile(
        db,
        current_user,
        profile
    )

    if not new_profile:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists."
        )

    return new_profile


# ==========================================================
# GET MY PROFILE
# ==========================================================

@router.get(
    "/me",
    response_model=ProfileResponse,
    summary="Obtener mi perfil",
    description="""
Obtiene el perfil del usuario autenticado.
"""
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = profile_service.get_my_profile(
        db,
        current_user
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    return profile


# ==========================================================
# UPDATE PROFILE
# ==========================================================

@router.put(
    "/me",
    response_model=ProfileResponse,
    summary="Actualizar mi perfil",
    description="""
Actualiza únicamente los campos enviados del perfil del usuario autenticado.
"""
)
def update_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = profile_service.update_my_profile(
        db,
        current_user,
        profile_data
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    return profile


# ==========================================================
# DELETE PROFILE
# ==========================================================

@router.delete(
    "/me",
    summary="Eliminar mi perfil",
    description="""
Elimina el perfil del usuario autenticado.
"""
)
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = profile_service.delete_my_profile(
        db,
        current_user
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    return {
        "message": "Profile deleted successfully."
    }