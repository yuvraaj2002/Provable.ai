from pydantic import BaseModel,Field

class CreateAPIKeyRequest(BaseModel):
    key_name:str = Field(...)