from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False
    )

    job_preferences = relationship(
    "JobPreference",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan"
)