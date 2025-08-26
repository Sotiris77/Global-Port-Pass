from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean
from app.db.base import Base

class AccessPasscode(Base):
    __tablename__ = "access_passcodes"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    code = Column(String(12), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
