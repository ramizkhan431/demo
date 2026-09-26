from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # These are in .env for docker but also for local reference
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    
    # Internal Security
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://192.168.0.171:8081",
        "http://192.168.0.171:8000",
        "https://travelchronicles.net",
        "https://www.travelchronicles.net",
        "http://187.127.146.136:8000"
    ]
    INTERNAL_API_KEY: str = "travel-blog-secret-key-123"




    # Storage Configuration (Local or S3)
    STORAGE_TYPE: str = "local" # or "s3"
    STORAGE_PATH: str = "uploads"

    # SMTP / Mail Settings
    SMTP_HOST: str = "smtp.hostinger.com"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = "info@travelchronicles.net"
    SMTP_PASSWORD: str = "Maroantsetra1!"
    SMTP_USE_SSL: bool = True
    MAIL_FROM_ADDRESS: Optional[str] = "info@travelchronicles.net"
    MAIL_FROM_NAME: str = "travelchronicles"
    MAIL_TO_ADDRESS: str = "info@travelchronicles.net"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore" # Ignore extra environment variables
    )

settings = Settings()
