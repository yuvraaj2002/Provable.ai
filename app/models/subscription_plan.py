import uuid
from app.core.database import Base
from sqlalchemy import Column, String, DateTime, Text,Integer,Float,JSON
from sqlalchemy.sql import func


class PlanDetails(Base):
    __tablename__ = "plan_details"

    id = Column(String,primary_key=True,default=lambda: str(uuid.uuid4()))
    plan_name = Column(String(10),nullable=False)
    price_cents = Column(Integer, nullable=False) 
    currency = Column(String(3), default="USD")
    api_requests = Column(Integer,nullable=False)
    features = Column(JSON,nullable=False)
    created_at = Column(DateTime,server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

