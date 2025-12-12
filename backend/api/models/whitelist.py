from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Whitelist(SQLModel, table=True):
    """Whitelisted IP addresses (bypass rate limiting)"""
    __tablename__ = "whitelist"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(unique=True, index=True, max_length=45)
    added_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "ip": "10.0.0.1"
            }
        }
