import io, uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.api.rbac import require_role
from app.models.document import Document
from app.models.passcode import AccessPasscode
from app.schemas.document import DocumentOut, PasscodeCreate, PasscodeVerify
from app.services.storage import upload_fileobj, generate_presigned_url
from app.services.audit import log_audit

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/", response_model=list[DocumentOut])
def list_my_documents(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Document).filter(Document.owner_id == user.id).order_by(Document.id.desc()).all()

@router.post("/upload", response_model=DocumentOut)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(require_role("vessel", "port", "admin"))):
    key = f"{user.id}/{uuid.uuid4()}-{file.filename}"
    data = io.BytesIO(file.file.read())
    upload_fileobj(data, key, file.content_type or "application/octet-stream")
    doc = Document(owner_id=user.id, filename=file.filename, content_type=file.content_type or "application/octet-stream", s3_key=key)
    db.add(doc); db.commit(); db.refresh(doc)
    log_audit(db, actor_id=user.id, action="upload_document", entity_type="document", entity_id=doc.id, meta={"filename": file.filename})
    return doc

@router.post("/{doc_id}/passcode", response_model=dict)
def create_passcode(doc_id: int, payload: PasscodeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.owner_id == user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    code = str(uuid.uuid4())[:6].upper()
    expires_at = datetime.utcnow() + timedelta(minutes=payload.expires_minutes)
    db.add(AccessPasscode(document_id=doc.id, code=code, expires_at=expires_at)); db.commit()
    log_audit(db, actor_id=user.id, action="create_passcode", entity_type="document", entity_id=doc.id, meta={"expires_minutes": payload.expires_minutes})
    return {"code": code, "expires_at": expires_at.isoformat() + "Z"}

@router.post("/{doc_id}/passcode/verify", response_model=dict)
def verify_passcode(doc_id: int, payload: PasscodeVerify, db: Session = Depends(get_db)):
    record = db.query(AccessPasscode).filter(
        AccessPasscode.document_id == doc_id,
        AccessPasscode.code == payload.code,
        AccessPasscode.used == False
    ).first()
    if not record:
        raise HTTPException(status_code=400, detail="Invalid code")
    if record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Code expired")
    record.used = True; db.commit()
    row = db.execute("SELECT s3_key, id FROM documents WHERE id = :id", {"id": doc_id}).first()
    url = generate_presigned_url(row[0], expires_in=300)
    log_audit(db, actor_id=None, action="verify_passcode", entity_type="document", entity_id=row[1], meta={"method": "one_time_url"})
    return {"download_url": url, "expires_in_seconds": 300}
