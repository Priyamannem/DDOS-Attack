from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class IPActivity(SQLModel, table=True):
    """Track IP activity and rate limiting data"""
    __tablename__ = "ip_activity"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    ip_address: str = Field(index=True, unique=True, max_length=45)
    requests_last_minute: int = Field(default=0)
    requests_last_second: int = Field(default=0)
    total_requests: int = Field(default=0)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    is_blocked: bool = Field(default=False)
    blocked_until: Optional[datetime] = Field(default=None)
    first_detected: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "ip_address": "192.168.1.100",
                "requests_last_minute": 50,
                "requests_last_second": 5,
                "total_requests": 1000,
                "is_blocked": False
            }
        }
