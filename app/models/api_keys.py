import uuid
from sqlalchemy import Column, String, DateTime, Text
from app.core.database import Base
from sqlalchemy.sql import func

class ApiKeys(Base):
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    key_name = Column(String, nullable=False)
    hash_key = Column(String(64), nullable=False, unique=True)
    last_4_digit = Column(String(4), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)