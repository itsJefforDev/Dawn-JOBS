"""
Servicio de perfiles.

Este módulo contiene toda la lógica de negocio relacionada con
el perfil profesional del usuario.

IMPORTANTE
----------
Todas las operaciones utilizan el usuario autenticado obtenido
desde el JWT.

Por motivos de seguridad nunca se recibe el user_id desde
el frontend.

Autor:
Job Bot Backend
"""

from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.models.user import User

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate
)


# ==========================================================
# CREATE PROFILE
# ==========================================================

def create_profile(
    db: Session,
    current_user: User,
    profile: ProfileCreate
):
    """
    Crea el perfil profesional del usuario autenticado.

    Parámetros
    ----------
    db : Session
        Sesión de SQLAlchemy.

    current_user : User
        Usuario autenticado obtenido mediante JWT.

    profile : ProfileCreate
        Información del perfil.

    Retorna
    -------
    Profile
        Perfil creado.

    Nota
    ----
    Un usuario únicamente puede tener un perfil.
    """

    existing_profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if existing_profile:
        return None

    new_profile = Profile(
        user_id=current_user.id,
        full_name=profile.full_name,
        title=profile.title,
        skills=profile.skills,
        experience=profile.experience,
        english_level=profile.english_level,
        location=profile.location,
        salary_expectation=profile.salary_expectation,
        work_mode=profile.work_mode
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


# ==========================================================
# GET MY PROFILE
# ==========================================================

def get_my_profile(
    db: Session,
    current_user: User
):
    """
    Obtiene el perfil del usuario autenticado.

    Nunca recibe profile_id.

    Retorna
    -------
    Profile | None
    """

    return db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()


# ==========================================================
# UPDATE PROFILE
# ==========================================================

def update_my_profile(
    db: Session,
    current_user: User,
    profile_data: ProfileUpdate
):
    """
    Actualiza el perfil del usuario autenticado.

    Sólo se actualizan los campos enviados.

    Retorna
    -------
    Profile | None
    """

    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if not profile:
        return None

    update_data = profile_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return profile


# ==========================================================
# DELETE PROFILE
# ==========================================================

def delete_my_profile(
    db: Session,
    current_user: User
):
    """
    Elimina el perfil del usuario autenticado.

    Retorna
    -------
    Profile | None
    """

    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if not profile:
        return None

    db.delete(profile)
    db.commit()

    return profile