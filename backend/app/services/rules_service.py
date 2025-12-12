from sqlmodel import Session, select
from app.models.rules import Rules
from datetime import datetime
from typing import Optional
from app.core.config import settings


class RulesService:
    """Service for managing DDoS protection rules"""
    
    @staticmethod
    def get_current_rules(session: Session) -> Rules:
        """Get current active rules (creates default if none exist)"""
        statement = select(Rules).order_by(Rules.updated_at.desc()).limit(1)
        rules = session.exec(statement).first()
        
        if not rules:
            rules = Rules(
                max_req_per_sec=settings.DEFAULT_MAX_REQ_PER_SEC,
                max_req_per_min=settings.DEFAULT_MAX_REQ_PER_MIN,
                block_duration=settings.DEFAULT_BLOCK_DURATION,
                anomaly_threshold=settings.DEFAULT_ANOMALY_THRESHOLD
            )
            session.add(rules)
            session.commit()
            session.refresh(rules)
        
        return rules
    
    @staticmethod
    def update_rules(
        session: Session,
        max_req_per_sec: Optional[int] = None,
        max_req_per_min: Optional[int] = None,
        block_duration: Optional[int] = None,
        anomaly_threshold: Optional[int] = None
    ) -> Rules:
        """Update protection rules"""
        current_rules = RulesService.get_current_rules(session)
        
        # Create new rule entry (keeping history)
        new_rules = Rules(
            max_req_per_sec=max_req_per_sec if max_req_per_sec is not None else current_rules.max_req_per_sec,
            max_req_per_min=max_req_per_min if max_req_per_min is not None else current_rules.max_req_per_min,
            block_duration=block_duration if block_duration is not None else current_rules.block_duration,
            anomaly_threshold=anomaly_threshold if anomaly_threshold is not None else current_rules.anomaly_threshold,
            updated_at=datetime.utcnow()
        )
        
        session.add(new_rules)
        session.commit()
        session.refresh(new_rules)
        
        return new_rules
