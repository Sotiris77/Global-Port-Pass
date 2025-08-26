from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    s3_key = Column(String(512), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
