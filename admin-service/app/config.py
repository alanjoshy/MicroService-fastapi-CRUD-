from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_NAME: str = "admin_service_db"
    
    # Application settings
    APP_NAME: str = "Admin Service"
    API_PREFIX: str = "/api/admin"
    
    # External service URLs
    AUTH_SERVICE_URL: str = "http://auth-service:8003"
    USER_SERVICE_URL: str = "http://user-service:8001"
    
    class Config:
        env_file = ".env"


settings = Settings()