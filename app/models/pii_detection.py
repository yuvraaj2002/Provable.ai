import uuid
from app.core.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column,String,DateTime,Boolean,Text,ForeignKey,JSON,Integer

class PII_Registeration(Base):
    __tablename__ = "pii_registration"

    id = Column(String,default = lambda:str(uuid.uuid4()),primary_key=True) 
    user_id = Column(String,ForeignKey("users.id"),nullable=False, index=True)
    endpoint_url = Column(String,nullable=False)
    bearer_token = Column(String,nullable=False)
    description = Column(Text,nullable=False)
    email_alert = Column(Boolean,nullable=False) 
    created_at = Column(DateTime,server_default=func.now(),nullable=False) 
    updated_at = Column(DateTime,server_default=func.now(), onupdate=func.now(),nullable=False)  


class PII_Results(Base):
    __tablename__ = "pii_results"

    id = Column(String,default = lambda:str(uuid.uuid4()),primary_key=True) 
    pi_reg_id = Column(String,ForeignKey("pii_registration.id"),index=True)
    generated_questions = Column(JSON,nullable=False)
    findings = Column(JSON,nullable=False)
    security_score = Column(Integer,nullable=False)
    status = Column(String,nullable=False,index=True)
    completed_at = Column(DateTime,server_default=func.now(),nullable=False) 

