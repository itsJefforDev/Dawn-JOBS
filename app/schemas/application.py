from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: str
    notes: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    notes: Optional[str]
    applied_at: datetime

    class Config:
        from_attributes = True