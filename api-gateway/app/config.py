from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "API Gateway"
    
    # Service URLs
    USER_SERVICE_URL: str = "http://user-service:8001"
    ADMIN_SERVICE_URL: str = "http://admin-service:8002"
    AUTH_SERVICE_URL: str = "http://auth-service:8003"
    PRODUCT_SERVICE_URL: str = "http://product-service:8004"
    
    class Config:
        env_file = ".env"


settings = Settings()