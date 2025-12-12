from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Log(SQLModel, table=True):
    """Request log entries"""
    __tablename__ = "logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    ip: str = Field(max_length=45, index=True)
    endpoint: str = Field(max_length=255)
    status: str = Field(max_length=50)  # allowed, blocked, suspicious
    reason: str = Field(max_length=255)
    
    class Config:
        json_schema_extra = {
            "example": {
                "ip": "192.168.1.100",
                "endpoint": "/api/data",
                "status": "allowed",
                "reason": "normal_traffic"
            }
        }
