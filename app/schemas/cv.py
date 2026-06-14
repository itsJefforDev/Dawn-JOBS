from pydantic import BaseModel


class CVResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str
    extracted_text: str | None

    class Config:
        from_attributes = True