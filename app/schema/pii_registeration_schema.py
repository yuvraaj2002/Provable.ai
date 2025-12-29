from pydantic import BaseModel, Field

class PIIRegisteration(BaseModel):
    endpoint_url: str = Field(..., description="Endpoint URL for PII registration")
    bearer_token: str = Field(..., description="Bearer token for authentication")
    description: str = Field(..., description="Purpose or details of registration")
    que_to_generate: int = Field(..., description="Number of items to generate in queue")
    email_alert: bool = Field(..., description="Enable email alert for registration")