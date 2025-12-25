from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    OPENAI_API_KEY: str
    CLIENT_ID:str
    CLIENT_SECRET:str
    SESSION_SECRET_KEY:str
    SECRET_KET:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )
        
settings = Settings()