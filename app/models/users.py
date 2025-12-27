import uuid
from sqlalchemy import Column, String, DateTime,Boolean
from app.core.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(255), primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    hashed_password = Column(String,nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True) 
    is_admin = Column(Boolean,default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PendingUser(Base):
    __tablename__ = "pending_users"

    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50),nullable=True)
    email = Column(String,nullable=False)
    hashed_password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    verification_token = Column(String,nullable=False)
