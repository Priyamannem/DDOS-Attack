from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TrafficStats(SQLModel, table=True):
    """Aggregated traffic statistics"""
    __tablename__ = "traffic_stats"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    requests_per_second: int = Field(default=0)
    requests_per_minute: int = Field(default=0)
    blocked_count: int = Field(default=0)
    suspicious_count: int = Field(default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "requests_per_second": 150,
                "requests_per_minute": 8000,
                "blocked_count": 25,
                "suspicious_count": 12
            }
        }
