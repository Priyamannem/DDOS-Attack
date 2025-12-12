from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Blacklist(SQLModel, table=True):
    """Blacklisted IP addresses"""
    __tablename__ = "blacklist"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(unique=True, index=True, max_length=45)
    reason: str = Field(max_length=255)
    added_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "ip": "203.0.113.0",
                "reason": "repeated_malicious_activity"
            }
        }
