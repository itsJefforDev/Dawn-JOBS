from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    full_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    skills = Column(Text, nullable=False)
    experience = Column(Integer, nullable=False)
    english_level = Column(String, nullable=False)
    location = Column(String, nullable=False)
    salary_expectation = Column(String, nullable=True)
    work_mode = Column(String, nullable=False)

    # created_at = Column(
    #     DateTime(timezone=True),
    #     server_default=func.now()
    # )

    # updated_at = Column(
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    #     onupdate=func.now()
    # )

    user = relationship(
        "User",
        back_populates="profile"
    )