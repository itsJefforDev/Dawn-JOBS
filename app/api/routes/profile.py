"""
Endpoints del módulo Profile.

Todos los endpoints requieren autenticación JWT.

El usuario se obtiene mediante:

    Depends(get_current_user)

Por seguridad, ningún endpoint recibe user_id
desde el frontend.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse
)

from app.services.profile_service import (
    create_profile,
    get_my_profile,
    update_my_profile,
    delete_my_profile
)


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


# ============================================================
# CREATE
# ============================================================

@router.post(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear mi perfil",
    description="""
Crea el perfil profesional del usuario autenticado.

El user_id NO se recibe desde el cliente.

El backend obtiene automáticamente el usuario mediante
el JWT enviado en el Header Authorization.

Un usuario solamente puede tener un perfil.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        409: {
            "description": "El usuario ya tiene un perfil"
        }
    }
)
def create_my_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crea el perfil del usuario autenticado.
    """

    profile = create_profile(
        db,
        current_user,
        profile_data
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists"
        )

    return profile


# ============================================================
# GET
# ============================================================

@router.get(
    "/me",
    response_model=ProfileResponse,
    summary="Obtener mi perfil",
    description="""
Obtiene el perfil perteneciente al usuario autenticado.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        404: {
            "description": "Perfil no encontrado"
        }
    }
)
def get_my_profile_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Devuelve el perfil del usuario autenticado.
    """

    profile = get_my_profile(
        db,
        current_user
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile


# ============================================================
# UPDATE
# ============================================================

@router.put(
    "/me",
    response_model=ProfileResponse,
    summary="Actualizar mi perfil",
    description="""
Actualiza los datos del perfil del usuario autenticado.

Sólo los campos enviados serán modificados.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        404: {
            "description": "Perfil no encontrado"
        }
    }
)
def update_my_profile_data(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza el perfil del usuario autenticado.
    """

    profile = update_my_profile(
        db,
        current_user,
        profile_data
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile


# ============================================================
# DELETE
# ============================================================

@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Eliminar mi perfil",
    description="""
Elimina permanentemente el perfil del usuario autenticado.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        404: {
            "description": "Perfil no encontrado"
        }
    }
)
def delete_my_profile_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Elimina el perfil del usuario autenticado.
    """

    profile = delete_my_profile(
        db,
        current_user
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return {
        "message": "Profile deleted successfully"
    }