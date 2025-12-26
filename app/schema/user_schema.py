from pydantic import BaseModel, Field, EmailStr, field_validator

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