from pydantic import BaseModel
from datetime import datetime


class AutoApplyResponse(BaseModel):
    job_id: int
    status: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True