from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Rules(SQLModel, table=True):
    """DDoS protection rules configuration"""
    __tablename__ = "rules"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    max_req_per_sec: int = Field(default=10)
    max_req_per_min: int = Field(default=100)
    block_duration: int = Field(default=300)  # seconds
    anomaly_threshold: int = Field(default=5000)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "max_req_per_sec": 10,
                "max_req_per_min": 100,
                "block_duration": 300,
                "anomaly_threshold": 5000
            }
        }
