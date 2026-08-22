"""
Servicio de gestión de perfiles.

Responsabilidades:

    - Crear perfiles.
    - Obtener el perfil del usuario autenticado.
    - Actualizar el perfil.
    - Eliminar el perfil.

IMPORTANTE:

Este servicio nunca recibe un user_id enviado por el frontend.

El user_id proviene del usuario autenticado mediante JWT.
"""

from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.models.user import User

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate
)


# ============================================================
# CREATE PROFILE
# ============================================================

def create_profile(
    db: Session,
    current_user: User,
    profile_data: ProfileCreate
):
    """
    Crea el perfil del usuario autenticado.

    Un usuario solamente puede tener un perfil.

    Parámetros
    ----------
    db:
        Sesión de SQLAlchemy.

    current_user:
        Usuario autenticado obtenido mediante JWT.

    profile_data:
        Datos del nuevo perfil.

    Returns
    -------
    Profile:
        Perfil creado.

    None:
        Si el usuario ya tiene un perfil.
    """

    # --------------------------------------------------------
    # Verificar si ya existe un perfil
    # --------------------------------------------------------

    existing_profile = (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )

    if existing_profile:
        return None

    # --------------------------------------------------------
    # Crear perfil
    # --------------------------------------------------------

    new_profile = Profile(
        user_id=current_user.id,

        full_name=profile_data.full_name,
        title=profile_data.title,
        skills=profile_data.skills,
        experience=profile_data.experience,
        english_level=profile_data.english_level,
        location=profile_data.location,
        salary_expectation=profile_data.salary_expectation,
        work_mode=profile_data.work_mode
    )

    # --------------------------------------------------------
    # Persistir
    # --------------------------------------------------------

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


# ============================================================
# GET MY PROFILE
# ============================================================

def get_my_profile(
    db: Session,
    current_user: User
):
    """
    Obtiene el perfil del usuario autenticado.

    Nunca utiliza profile_id ni user_id enviados desde
    el cliente.
    """

    return (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )


# ============================================================
# UPDATE MY PROFILE
# ============================================================

def update_my_profile(
    db: Session,
    current_user: User,
    profile_data: ProfileUpdate
):
    """
    Actualiza el perfil del usuario autenticado.

    Permite actualización parcial.

    Sólo los campos enviados en la petición serán modificados.
    """

    profile = (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        return None

    # --------------------------------------------------------
    # Obtener únicamente los campos enviados
    # --------------------------------------------------------

    update_data = profile_data.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Aplicar cambios
    # --------------------------------------------------------

    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile


# ============================================================
# DELETE MY PROFILE
# ============================================================

def delete_my_profile(
    db: Session,
    current_user: User
):
    """
    Elimina el perfil del usuario autenticado.
    """

    profile = (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        return None

    db.delete(profile)
    db.commit()

    return profile