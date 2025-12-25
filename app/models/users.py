from sqlalchemy import Column, String, DateTime
from app.core.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(255), primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
