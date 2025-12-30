from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL:str
    DATABASE_URL_SYNC: str
    MAX_CHUNKS:int
    MAX_TOKEN_PER_CHUNK:int
    OPENAI_API_KEY: str
    CLIENT_ID:str
    CLIENT_SECRET:str
    SESSION_SECRET_KEY:str
    SECRET_KET:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    BREVO_API_KEY: str
    SENDER_NAME:str
    SENDER_EMAIL:str
    FRONTEND_BASE_URL: str = "http://localhost:8080"  # Default frontend URL for verification links
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )
        
settings = Settings()