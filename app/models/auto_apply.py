from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class AutoApplyLog(Base):
    __tablename__ = "auto_apply_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String, default="pending")
    message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())