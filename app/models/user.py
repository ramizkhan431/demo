from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    totp_secret = Column(String(32), nullable=True)
    is_totp_enabled = Column(Boolean, default=False)
