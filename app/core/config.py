from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL:str
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
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