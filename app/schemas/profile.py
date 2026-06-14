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


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    title: str | None = None
    skills: str | None = None
    experience: int | None = None
    english_level: str | None = None
    location: str | None = None
    salary_expectation: str | None = None
    work_mode: str | None = None