"""Environment Configuration"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "Play House Management System"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://playhouse:playhouse123@localhost:5432/playhouse_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
    ]
    
    # Business Settings
    BUSINESS_NAME: str = "Play House Gaming Center"
    CURRENCY: str = "SAR"
    DEFAULT_HOURLY_RATE: float = 50.0
    TAX_RATE: float = 0.15
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()

settings = get_settings()
