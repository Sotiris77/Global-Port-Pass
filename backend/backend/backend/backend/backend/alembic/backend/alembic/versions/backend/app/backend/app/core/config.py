from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Global Port Pass"
    env: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 60

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "db"
    postgres_port: int = 5432

    s3_endpoint_url: str
    s3_bucket: str
    s3_region: str = "us-east-1"
    s3_access_key: str
    s3_secret_key: str
    s3_use_ssl: bool = False

    admin_email: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()
