import boto3
from botocore.client import Config
from app.core.config import settings

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
        config=Config(signature_version="s3v4"),
    )

def upload_fileobj(fileobj, key: str, content_type: str):
    s3 = get_s3_client()
    s3.upload_fileobj(fileobj, settings.s3_bucket, key, ExtraArgs={"ContentType": content_type})

def generate_presigned_url(key: str, expires_in: int = 600) -> str:
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket, "Key": key},
        ExpiresIn=expires_in
    )
