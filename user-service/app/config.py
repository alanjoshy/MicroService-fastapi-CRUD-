from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_NAME: str = "user_service_db"
    
    # Application settings
    APP_NAME: str = "User Service"
    API_PREFIX: str = "/api/users"
    
    # Auth service URL for validation
    AUTH_SERVICE_URL: str = "http://auth-service:8003"
    
    class Config:
        env_file = ".env"


settings = Settings()