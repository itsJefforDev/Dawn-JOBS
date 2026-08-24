"""
Schemas de las vacantes.

JobResponse:
    Información que puede recibir el frontend.

JobMatchResponse:
    Información de una vacante junto con el resultado
    del matching del usuario.
"""

from datetime import datetime

from pydantic import BaseModel


# ============================================================
# JOB RESPONSE
# ============================================================

class JobResponse(BaseModel):
    """
    Representación pública de una vacante.
    """

    id: int
    external_id: str | None

    title: str
    company: str

    description: str | None

    location: str | None
    modality: str | None

    salary: int | None

    seniority: str | None
    employment_type: str | None

    source: str | None
    url: str | None

    posted_at: datetime | None

    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


# ============================================================
# JOB MATCH RESPONSE
# ============================================================

class JobMatchResponse(BaseModel):
    """
    Vacante acompañada de información de compatibilidad.

    match:
        True si cumple el criterio definido por el motor.

    score:
        Porcentaje aproximado de compatibilidad.
    """

    job: JobResponse
    match: bool
    score: int