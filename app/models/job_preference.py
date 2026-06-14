from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class JobPreference(Base):
    __tablename__ = "job_preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    role = Column(String, nullable=False)
    salary_min = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    modality = Column(String, nullable=True)  # remote, hybrid, onsite
    seniority = Column(String, nullable=True)  # junior, mid, senior
    tech_stack = Column(String, nullable=True)

    user = relationship("User")