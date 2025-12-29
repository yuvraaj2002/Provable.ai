import uuid
from app.core.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Text, JSON, Integer, ForeignKey,DateTime

class AgentFaithfullness(Base):
    __tablename__ = "agent_faithfullness"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False, index=True)
    query = Column(Text, nullable=False)
    context_retrieved = Column(JSON, nullable=False)
    response = Column(Text, nullable=False)
    verification_claims = Column(JSON, nullable=False)
    total_claims = Column(Integer, nullable=False)
    supported_claims = Column(Integer, nullable=False)
    non_supported_claims = Column(Integer, nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)