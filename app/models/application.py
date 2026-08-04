from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    # Usuario propietario de la postulación
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Vacante a la que aplicó
    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    # Estado actual de la aplicación
    status = Column(
        String,
        default="saved"
    )

    # Notas adicionales
    notes = Column(
        String,
        nullable=True
    )

    # Fecha de creación
    applied_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )