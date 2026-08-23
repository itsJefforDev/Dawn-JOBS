"""
Endpoints de preferencias laborales.

Todos los endpoints requieren autenticación JWT.

El usuario se obtiene mediante:

    Depends(get_current_user)

Nunca se recibe user_id desde el frontend.
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

from app.schemas.job_preference import (
    JobPreferenceCreate,
    JobPreferenceUpdate,
    JobPreferenceResponse
)

from app.services.job_preference_service import (
    create_preferences,
    get_my_preferences,
    update_my_preferences,
    delete_my_preferences,
    delete_preference_field
)


router = APIRouter(
    prefix="/preferences",
    tags=["Job Preferences"]
)


# ============================================================
# CREATE
# ============================================================

@router.post(
    "/me",
    response_model=JobPreferenceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear mis preferencias",
    description="""
Crea las preferencias laborales del usuario autenticado.

El user_id no se recibe desde el cliente.
Se obtiene automáticamente desde el JWT.

Cada usuario puede tener un único registro de preferencias.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        409: {
            "description": "Las preferencias ya existen"
        }
    }
)
def create_my_preferences(
    data: JobPreferenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crea las preferencias del usuario autenticado.
    """

    preferences = create_preferences(
        db,
        current_user,
        data
    )

    if preferences is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Preferences already exist"
        )

    return preferences


# ============================================================
# GET
# ============================================================

@router.get(
    "/me",
    response_model=JobPreferenceResponse,
    summary="Obtener mis preferencias",
    description="""
Obtiene las preferencias laborales del usuario autenticado.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        404: {
            "description": "Preferencias no encontradas"
        }
    }
)
def get_my_preferences_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Devuelve las preferencias del usuario autenticado.
    """

    preferences = get_my_preferences(
        db,
        current_user
    )

    if preferences is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )

    return preferences


# ============================================================
# UPDATE
# ============================================================

@router.put(
    "/me",
    response_model=JobPreferenceResponse,
    summary="Actualizar mis preferencias",
    description="""
Actualiza parcialmente las preferencias del usuario autenticado.

Sólo los campos enviados serán modificados.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        404: {
            "description": "Preferencias no encontradas"
        }
    }
)
def update_my_preferences_data(
    data: JobPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza las preferencias del usuario autenticado.
    """

    preferences = update_my_preferences(
        db,
        current_user,
        data
    )

    if preferences is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )

    return preferences


# ============================================================
# DELETE ALL
# ============================================================

@router.delete(
    "/me",
    summary="Eliminar mis preferencias",
    description="""
Elimina completamente las preferencias del usuario autenticado.
""",
    responses={
        401: {
            "description": "Usuario no autenticado"
        },
        404: {
            "description": "Preferencias no encontradas"
        }
    }
)
def delete_my_preferences_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Elimina todas las preferencias del usuario autenticado.
    """

    preferences = delete_my_preferences(
        db,
        current_user
    )

    if preferences is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )

    return {
        "message": "Preferences deleted successfully"
    }


# ============================================================
# DELETE ONE FIELD
# ============================================================

@router.delete(
    "/me/field/{field}",
    response_model=JobPreferenceResponse,
    summary="Limpiar una preferencia específica",
    description="""
Limpia el valor de un campo específico de las preferencias.

Campos permitidos:

    - salary_min
    - location
    - modality
    - seniority
    - tech_stack

El campo role no puede eliminarse porque es el criterio
principal de búsqueda.
""",
    responses={
        400: {
            "description": "Campo no permitido"
        },
        401: {
            "description": "Usuario no autenticado"
        },
        404: {
            "description": "Preferencias no encontradas"
        }
    }
)
def delete_my_preference_field(
    field: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Limpia un campo específico de las preferencias.
    """

    result = delete_preference_field(
        db,
        current_user,
        field
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )

    if result == "INVALID_FIELD":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid field. Allowed fields: "
                "salary_min, location, modality, "
                "seniority, tech_stack"
            )
        )

    return result