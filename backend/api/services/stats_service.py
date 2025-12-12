from sqlmodel import Session, select
from app.models.traffic_stats import TrafficStats
from datetime import datetime, timedelta
from typing import List


class StatsService:
    """Service for traffic statistics"""
    
    @staticmethod
    def record_stats(
        session: Session,
        requests_per_second: int,
        requests_per_minute: int,
        blocked_count: int,
        suspicious_count: int
    ) -> TrafficStats:
        """Record traffic statistics snapshot"""
        stats = TrafficStats(
            timestamp=datetime.utcnow(),
            requests_per_second=requests_per_second,
            requests_per_minute=requests_per_minute,
            blocked_count=blocked_count,
            suspicious_count=suspicious_count
        )
        session.add(stats)
        session.commit()
        session.refresh(stats)
        return stats
    
    @staticmethod
    def get_recent_stats(session: Session, minutes: int = 60) -> List[TrafficStats]:
        """Get statistics from the last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        statement = select(TrafficStats).where(
            TrafficStats.timestamp >= cutoff_time
        ).order_by(TrafficStats.timestamp.desc())
        
        return list(session.exec(statement).all())
    
    @staticmethod
    def get_latest_stats(session: Session) -> TrafficStats:
        """Get the most recent statistics entry"""
        statement = select(TrafficStats).order_by(TrafficStats.timestamp.desc()).limit(1)
        stats = session.exec(statement).first()
        
        if not stats:
            # Return default empty stats
            stats = TrafficStats(
                requests_per_second=0,
                requests_per_minute=0,
                blocked_count=0,
                suspicious_count=0
            )
        
        return stats
