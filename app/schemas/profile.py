"""
Schemas relacionados con el perfil profesional del usuario.

ProfileCreate:
    Datos necesarios para crear un perfil.

ProfileUpdate:
    Datos que pueden modificarse posteriormente.
    Todos son opcionales para permitir actualizaciones parciales.

ProfileResponse:
    Representación pública del perfil almacenado.
"""

from datetime import datetime

from pydantic import BaseModel, Field


# ============================================================
# CREATE
# ============================================================

class ProfileCreate(BaseModel):
    """
    Datos requeridos para crear un perfil.

    user_id NO forma parte de este schema.

    El usuario se obtiene automáticamente desde el JWT.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    title: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    skills: str = Field(
        ...,
        min_length=1
    )

    experience: int = Field(
        ...,
        ge=0
    )

    english_level: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    location: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    salary_expectation: str | None = Field(
        default=None,
        max_length=100
    )

    work_mode: str = Field(
        ...,
        min_length=1,
        max_length=50
    )


# ============================================================
# UPDATE
# ============================================================

class ProfileUpdate(BaseModel):
    """
    Datos que pueden actualizarse del perfil.

    Todos los campos son opcionales porque el usuario
    puede actualizar únicamente una parte del perfil.
    """

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    skills: str | None = None

    experience: int | None = Field(
        default=None,
        ge=0
    )

    english_level: str | None = Field(
        default=None,
        max_length=50
    )

    location: str | None = Field(
        default=None,
        max_length=150
    )

    salary_expectation: str | None = Field(
        default=None,
        max_length=100
    )

    work_mode: str | None = Field(
        default=None,
        max_length=50
    )


# ============================================================
# RESPONSE
# ============================================================

class ProfileResponse(BaseModel):
    """
    Información del perfil devuelta al cliente.
    """

    id: int
    user_id: int

    full_name: str
    title: str
    skills: str
    experience: int
    english_level: str
    location: str
    salary_expectation: str | None
    work_mode: str

    # created_at: datetime
    # updated_at: datetime | None

    class Config:
        from_attributes = True