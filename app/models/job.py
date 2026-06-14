from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    modality = Column(String, nullable=True)
    salary = Column(Integer, nullable=True)
    source = Column(String, nullable=True)
    url = Column(String, nullable=True)