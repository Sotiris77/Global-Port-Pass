from sqlalchemy.orm import Session
from app.models.audit import AuditLog

def log_audit(db: Session, *, actor_id: int | None, action: str, entity_type: str, entity_id: int | None, meta: dict | None = None):
    db.add(AuditLog(actor_id=actor_id, action=action, entity_type=entity_type, entity_id=entity_id, meta=meta or {}))
    db.commit()
