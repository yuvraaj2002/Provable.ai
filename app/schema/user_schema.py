from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)
    username: str = Field(...)

    @field_validator('username')
    @classmethod
    def username_must_not_contain_double_underscore(cls, v: str) -> str:
        if '__' in v:
            raise ValueError('username must not contain double underscores ("__")')
        return v

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    last_login: Optional[datetime] = None
    is_admin: bool = False
    created_at: datetime
    updated_at: datetime
    
    @field_validator('is_admin', mode='before')
    @classmethod
    def validate_is_admin(cls, v):
        if v is None:
            return False
        return bool(v)
    
    class Config:
        from_attributes = True