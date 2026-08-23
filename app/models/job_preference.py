"""
Modelo de preferencias laborales del usuario.

Cada usuario puede tener una única configuración de
preferencias laborales.

Relación:

    User 1 ───────── 1 JobPreference
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class JobPreference(Base):
    __tablename__ = "job_preferences"

    # ========================================================
    # PRIMARY KEY
    # ========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ========================================================
    # USER RELATIONSHIP
    # ========================================================

    """
    Identifica al propietario de las preferencias.

    IMPORTANTE:
        Este valor NO será recibido desde el frontend.

        El backend lo obtendrá mediante:

            current_user.id

    unique=True garantiza que un usuario no pueda tener
    múltiples registros de preferencias.
    """

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    # ========================================================
    # PREFERENCES
    # ========================================================

    # Cargo o rol deseado.
    role = Column(
        String,
        nullable=False
    )

    # Salario mínimo esperado.
    salary_min = Column(
        Integer,
        nullable=True
    )

    # Ubicación deseada.
    location = Column(
        String,
        nullable=True
    )

    # Modalidad:
    # remote / hybrid / onsite
    modality = Column(
        String,
        nullable=True
    )

    # Seniority:
    # junior / mid / senior
    seniority = Column(
        String,
        nullable=True
    )

    # Tecnologías deseadas.
    tech_stack = Column(
        String,
        nullable=True
    )

    # ========================================================
    # RELATIONSHIP
    # ========================================================

    user = relationship(
        "User",
        back_populates="job_preferences"
    )