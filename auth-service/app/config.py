from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # JWT settings
    SECRET_KEY: str = "your-secret-key-for-jwt-should-be-very-long-and-secure"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application settings
    APP_NAME: str = "Auth Service"
    API_PREFIX: str = "/api/auth"
    
    # User service URL
    USER_SERVICE_URL: str = "http://user-service:8001"
    
    class Config:
        env_file = ".env"


settings = Settings()