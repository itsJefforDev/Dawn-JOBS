from pydantic import BaseModel
from typing import Optional


class JobPreferenceCreate(BaseModel):
    role: str
    salary_min: Optional[int] = None
    location: Optional[str] = None
    modality: Optional[str] = None
    seniority: Optional[str] = None
    tech_stack: Optional[str] = None


class JobPreferenceUpdate(BaseModel):
    role: Optional[str] = None
    salary_min: Optional[int] = None
    location: Optional[str] = None
    modality: Optional[str] = None
    seniority: Optional[str] = None
    tech_stack: Optional[str] = None


class JobPreferenceResponse(BaseModel):
    id: int
    user_id: int
    role: str
    salary_min: Optional[int]
    location: Optional[str]
    modality: Optional[str]
    seniority: Optional[str]
    tech_stack: Optional[str]

    class Config:
        from_attributes = True