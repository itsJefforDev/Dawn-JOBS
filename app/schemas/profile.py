from pydantic import BaseModel


class ProfileCreate(BaseModel):
    full_name: str
    title: str
    skills: str
    experience: int
    english_level: str
    location: str
    salary_expectation: str | None = None
    work_mode: str


class ProfileResponse(ProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True