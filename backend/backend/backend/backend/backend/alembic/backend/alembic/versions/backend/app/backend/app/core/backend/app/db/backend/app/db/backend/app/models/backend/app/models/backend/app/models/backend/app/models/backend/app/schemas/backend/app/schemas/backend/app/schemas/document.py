from pydantic import BaseModel

class DocumentOut(BaseModel):
    id: int
    filename: str
    content_type: str
    s3_key: str
    class Config:
        from_attributes = True

class PasscodeCreate(BaseModel):
    expires_minutes: int = 10

class PasscodeVerify(BaseModel):
    code: str
