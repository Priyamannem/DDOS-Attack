from sqlmodel import Session, select
from app.models.logs import Log
from datetime import datetime
from typing import List, Optional


class LogsService:
    """Service for managing request logs"""
    
    @staticmethod
    def create_log(
        session: Session,
        ip: str,
        endpoint: str,
        status: str,
        reason: str
    ) -> Log:
        """Create a new log entry"""
        log = Log(
            timestamp=datetime.utcnow(),
            ip=ip,
            endpoint=endpoint,
            status=status,
            reason=reason
        )
        session.add(log)
        session.commit()
        session.refresh(log)
        return log
    
    @staticmethod
    def get_recent_logs(session: Session, limit: int = 200) -> List[Log]:
        """Get recent log entries"""
        statement = select(Log).order_by(Log.timestamp.desc()).limit(limit)
        return list(session.exec(statement).all())
    
    @staticmethod
    def get_logs_by_ip(session: Session, ip: str, limit: int = 100) -> List[Log]:
        """Get logs for a specific IP"""
        statement = select(Log).where(Log.ip == ip).order_by(Log.timestamp.desc()).limit(limit)
        return list(session.exec(statement).all())
    
    @staticmethod
    def get_logs_by_status(session: Session, status: str, limit: int = 200) -> List[Log]:
        """Get logs by status (allowed, blocked, suspicious)"""
        statement = select(Log).where(Log.status == status).order_by(Log.timestamp.desc()).limit(limit)
        return list(session.exec(statement).all())
    
    @staticmethod
    def count_logs_by_status(session: Session, status: str) -> int:
        """Count logs by status"""
        statement = select(Log).where(Log.status == status)
        return len(list(session.exec(statement).all()))
