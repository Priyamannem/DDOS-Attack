from pydantic_settings import BaseSettings
from typing import Optional, Union
from pydantic import field_validator


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Application
    APP_NAME: str = "DDoS Prevention System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ddos_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting Defaults
    DEFAULT_MAX_REQ_PER_SEC: int = 10
    DEFAULT_MAX_REQ_PER_MIN: int = 100
    DEFAULT_BLOCK_DURATION: int = 300  # 5 minutes in seconds
    DEFAULT_ANOMALY_THRESHOLD: int = 5000
    
    # Redis (Optional)
    REDIS_URL: Optional[str] = None
    USE_REDIS: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/traffic.log"
    
    # CORS - accepts both list and comma-separated string
    CORS_ORIGINS: Union[list, str] = ["http://localhost:3000", "http://localhost:5173"]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
