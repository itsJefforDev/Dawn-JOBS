from pydantic import BaseModel
from typing import Optional


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: Optional[str]
    modality: Optional[str]
    salary: Optional[int]
    source: Optional[str]
    url: Optional[str]

    class Config:
        from_attributes = True