from sqlmodel import Session, select
from app.models.ip_activity import IPActivity
from datetime import datetime
from typing import Optional
from app.core.utils import is_blocked_active, calculate_block_until


class IPService:
    """Service for managing IP activity"""
    
    @staticmethod
    def get_or_create_ip(session: Session, ip_address: str) -> IPActivity:
        """Get existing IP activity or create new record"""
        statement = select(IPActivity).where(IPActivity.ip_address == ip_address)
        ip_activity = session.exec(statement).first()
        
        if not ip_activity:
            ip_activity = IPActivity(
                ip_address=ip_address,
                first_detected=datetime.utcnow(),
                last_seen=datetime.utcnow()
            )
            session.add(ip_activity)
            session.commit()
            session.refresh(ip_activity)
        
        return ip_activity
    
    @staticmethod
    def update_request_count(session: Session, ip_address: str) -> IPActivity:
        """Increment request counters for an IP"""
        ip_activity = IPService.get_or_create_ip(session, ip_address)
        
        ip_activity.requests_last_second += 1
        ip_activity.requests_last_minute += 1
        ip_activity.total_requests += 1
        ip_activity.last_seen = datetime.utcnow()
        
        session.add(ip_activity)
        session.commit()
        session.refresh(ip_activity)
        
        return ip_activity
    
    @staticmethod
    def block_ip(session: Session, ip_address: str, duration_seconds: int, reason: str = "rate_limit_exceeded") -> IPActivity:
        """Block an IP address"""
        ip_activity = IPService.get_or_create_ip(session, ip_address)
        
        ip_activity.is_blocked = True
        ip_activity.blocked_until = calculate_block_until(duration_seconds)
        
        session.add(ip_activity)
        session.commit()
        session.refresh(ip_activity)
        
        return ip_activity
    
    @staticmethod
    def unblock_ip(session: Session, ip_address: str) -> Optional[IPActivity]:
        """Unblock an IP address"""
        statement = select(IPActivity).where(IPActivity.ip_address == ip_address)
        ip_activity = session.exec(statement).first()
        
        if ip_activity:
            ip_activity.is_blocked = False
            ip_activity.blocked_until = None
            
            session.add(ip_activity)
            session.commit()
            session.refresh(ip_activity)
        
        return ip_activity
    
    @staticmethod
    def is_ip_blocked(session: Session, ip_address: str) -> bool:
        """Check if IP is currently blocked"""
        statement = select(IPActivity).where(IPActivity.ip_address == ip_address)
        ip_activity = session.exec(statement).first()
        
        if not ip_activity or not ip_activity.is_blocked:
            return False
        
        # Check if block has expired
        if not is_blocked_active(ip_activity.blocked_until):
            IPService.unblock_ip(session, ip_address)
            return False
        
        return True
    
    @staticmethod
    def get_blocked_ips(session: Session) -> list[IPActivity]:
        """Get all currently blocked IPs"""
        statement = select(IPActivity).where(IPActivity.is_blocked == True)
        return list(session.exec(statement).all())
    
    @staticmethod
    def reset_counters(session: Session, ip_address: str, reset_type: str = "second"):
        """Reset rate limiting counters"""
        statement = select(IPActivity).where(IPActivity.ip_address == ip_address)
        ip_activity = session.exec(statement).first()
        
        if ip_activity:
            if reset_type == "second":
                ip_activity.requests_last_second = 0
            elif reset_type == "minute":
                ip_activity.requests_last_minute = 0
                ip_activity.requests_last_second = 0
            
            session.add(ip_activity)
            session.commit()
