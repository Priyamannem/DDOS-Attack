from sqlmodel import Session, select
from app.models.blacklist import Blacklist
from app.models.whitelist import Whitelist
from datetime import datetime
from typing import List, Optional


class TrafficService:
    """Service for blacklist/whitelist management"""
    
    # Blacklist operations
    @staticmethod
    def add_to_blacklist(session: Session, ip: str, reason: str) -> Blacklist:
        """Add IP to blacklist"""
        # Check if already exists
        statement = select(Blacklist).where(Blacklist.ip == ip)
        existing = session.exec(statement).first()
        
        if existing:
            # Update reason
            existing.reason = reason
            existing.added_at = datetime.utcnow()
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing
        
        # Create new entry
        blacklist_entry = Blacklist(
            ip=ip,
            reason=reason,
            added_at=datetime.utcnow()
        )
        session.add(blacklist_entry)
        session.commit()
        session.refresh(blacklist_entry)
        return blacklist_entry
    
    @staticmethod
    def remove_from_blacklist(session: Session, ip: str) -> bool:
        """Remove IP from blacklist"""
        statement = select(Blacklist).where(Blacklist.ip == ip)
        entry = session.exec(statement).first()
        
        if entry:
            session.delete(entry)
            session.commit()
            return True
        return False
    
    @staticmethod
    def is_blacklisted(session: Session, ip: str) -> bool:
        """Check if IP is blacklisted"""
        statement = select(Blacklist).where(Blacklist.ip == ip)
        return session.exec(statement).first() is not None
    
    @staticmethod
    def get_all_blacklisted(session: Session) -> List[Blacklist]:
        """Get all blacklisted IPs"""
        statement = select(Blacklist).order_by(Blacklist.added_at.desc())
        return list(session.exec(statement).all())
    
    # Whitelist operations
    @staticmethod
    def add_to_whitelist(session: Session, ip: str) -> Whitelist:
        """Add IP to whitelist"""
        # Check if already exists
        statement = select(Whitelist).where(Whitelist.ip == ip)
        existing = session.exec(statement).first()
        
        if existing:
            return existing
        
        # Create new entry
        whitelist_entry = Whitelist(
            ip=ip,
            added_at=datetime.utcnow()
        )
        session.add(whitelist_entry)
        session.commit()
        session.refresh(whitelist_entry)
        return whitelist_entry
    
    @staticmethod
    def remove_from_whitelist(session: Session, ip: str) -> bool:
        """Remove IP from whitelist"""
        statement = select(Whitelist).where(Whitelist.ip == ip)
        entry = session.exec(statement).first()
        
        if entry:
            session.delete(entry)
            session.commit()
            return True
        return False
    
    @staticmethod
    def is_whitelisted(session: Session, ip: str) -> bool:
        """Check if IP is whitelisted"""
        statement = select(Whitelist).where(Whitelist.ip == ip)
        return session.exec(statement).first() is not None
    
    @staticmethod
    def get_all_whitelisted(session: Session) -> List[Whitelist]:
        """Get all whitelisted IPs"""
        statement = select(Whitelist).order_by(Whitelist.added_at.desc())
        return list(session.exec(statement).all())
