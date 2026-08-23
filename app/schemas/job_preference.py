"""
Schemas de preferencias laborales.

JobPreferenceCreate:
    Se utiliza para crear las preferencias.

JobPreferenceUpdate:
    Permite actualizar parcialmente las preferencias.

JobPreferenceResponse:
    Datos devueltos por la API.

IMPORTANTE:
    Ningún schema recibe user_id desde el frontend.
"""

from pydantic import BaseModel, Field


# ============================================================
# CREATE
# ============================================================

class JobPreferenceCreate(BaseModel):
    """
    Datos necesarios para crear las preferencias del
    usuario autenticado.
    """

    role: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    salary_min: int | None = Field(
        default=None,
        ge=0
    )

    location: str | None = Field(
        default=None,
        max_length=150
    )

    modality: str | None = Field(
        default=None,
        max_length=50
    )

    seniority: str | None = Field(
        default=None,
        max_length=50
    )

    tech_stack: str | None = Field(
        default=None,
        max_length=500
    )


# ============================================================
# UPDATE
# ============================================================

class JobPreferenceUpdate(BaseModel):
    """
    Permite actualizar solamente los campos enviados.
    """

    role: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    salary_min: int | None = Field(
        default=None,
        ge=0
    )

    location: str | None = Field(
        default=None,
        max_length=150
    )

    modality: str | None = Field(
        default=None,
        max_length=50
    )

    seniority: str | None = Field(
        default=None,
        max_length=50
    )

    tech_stack: str | None = Field(
        default=None,
        max_length=500
    )


# ============================================================
# RESPONSE
# ============================================================

class JobPreferenceResponse(BaseModel):
    """
    Información de las preferencias almacenadas.
    """

    id: int
    user_id: int

    role: str
    salary_min: int | None
    location: str | None
    modality: str | None
    seniority: str | None
    tech_stack: str | None

    class Config:
        from_attributes = True