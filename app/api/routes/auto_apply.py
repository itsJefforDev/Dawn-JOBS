from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auto_apply_service import auto_apply_jobs

router = APIRouter(
    prefix="/auto-apply",
    tags=["Auto Apply"]
)


@router.post("/auto-apply/{user_id}")
async def auto_apply(user_id: int, db: Session = Depends(get_db)):
    return await auto_apply_jobs(db, user_id)