"""
Servicio de preferencias laborales.

Responsabilidades:

    - Crear preferencias.
    - Obtener las preferencias del usuario autenticado.
    - Actualizar preferencias.
    - Eliminar preferencias.
    - Eliminar un campo individual de preferencias.

IMPORTANTE:

    El user_id nunca proviene del frontend.

    Se obtiene mediante:

        current_user.id
"""

from sqlalchemy.orm import Session

from app.models.job_preference import JobPreference
from app.models.user import User

from app.schemas.job_preference import (
    JobPreferenceCreate,
    JobPreferenceUpdate
)


# ============================================================
# CREATE
# ============================================================

def create_preferences(
    db: Session,
    current_user: User,
    data: JobPreferenceCreate
):
    """
    Crea las preferencias del usuario autenticado.

    Un usuario sólo puede tener un registro de preferencias.

    Returns:
        JobPreference:
            Preferencias creadas.

        None:
            Si ya existen preferencias.
    """

    # --------------------------------------------------------
    # Verificar si ya existen preferencias
    # --------------------------------------------------------

    existing_preferences = (
        db.query(JobPreference)
        .filter(
            JobPreference.user_id == current_user.id
        )
        .first()
    )

    if existing_preferences:
        return None

    # --------------------------------------------------------
    # Crear preferencias
    # --------------------------------------------------------

    preferences = JobPreference(
        user_id=current_user.id,
        role=data.role,
        salary_min=data.salary_min,
        location=data.location,
        modality=data.modality,
        seniority=data.seniority,
        tech_stack=data.tech_stack
    )

    # --------------------------------------------------------
    # Persistir
    # --------------------------------------------------------

    db.add(preferences)
    db.commit()
    db.refresh(preferences)

    return preferences


# ============================================================
# GET MY PREFERENCES
# ============================================================

def get_my_preferences(
    db: Session,
    current_user: User
):
    """
    Obtiene las preferencias del usuario autenticado.
    """

    return (
        db.query(JobPreference)
        .filter(
            JobPreference.user_id == current_user.id
        )
        .first()
    )


# ============================================================
# UPDATE MY PREFERENCES
# ============================================================

def update_my_preferences(
    db: Session,
    current_user: User,
    data: JobPreferenceUpdate
):
    """
    Actualiza parcialmente las preferencias del usuario
    autenticado.

    Sólo los campos enviados serán modificados.
    """

    preferences = (
        db.query(JobPreference)
        .filter(
            JobPreference.user_id == current_user.id
        )
        .first()
    )

    if not preferences:
        return None

    # --------------------------------------------------------
    # Obtener sólo los campos enviados
    # --------------------------------------------------------

    update_data = data.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Aplicar cambios
    # --------------------------------------------------------

    for field, value in update_data.items():
        setattr(preferences, field, value)

    db.commit()
    db.refresh(preferences)

    return preferences


# ============================================================
# DELETE MY PREFERENCES
# ============================================================

def delete_my_preferences(
    db: Session,
    current_user: User
):
    """
    Elimina todas las preferencias del usuario autenticado.
    """

    preferences = (
        db.query(JobPreference)
        .filter(
            JobPreference.user_id == current_user.id
        )
        .first()
    )

    if not preferences:
        return None

    db.delete(preferences)
    db.commit()

    return preferences


# ============================================================
# DELETE ONE FIELD
# ============================================================

def delete_preference_field(
    db: Session,
    current_user: User,
    field: str
):
    """
    Elimina el contenido de un campo específico de las
    preferencias del usuario autenticado.

    Ejemplos:

        DELETE /preferences/me/field/location
        DELETE /preferences/me/field/tech_stack

    Nunca permite modificar campos fuera de la lista permitida.
    """

    preferences = (
        db.query(JobPreference)
        .filter(
            JobPreference.user_id == current_user.id
        )
        .first()
    )

    if not preferences:
        return None

    # --------------------------------------------------------
    # Campos que pueden ser limpiados
    # --------------------------------------------------------

    allowed_fields = {
        "salary_min",
        "location",
        "modality",
        "seniority",
        "tech_stack"
    }

    if field not in allowed_fields:
        return "INVALID_FIELD"

    # --------------------------------------------------------
    # Limpiar campo
    # --------------------------------------------------------

    setattr(
        preferences,
        field,
        None
    )

    db.commit()
    db.refresh(preferences)

    return preferences