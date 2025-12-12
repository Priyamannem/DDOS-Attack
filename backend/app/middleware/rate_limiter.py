from fastapi import Request, HTTPException
from sqlmodel import Session
from app.services.ip_service import IPService
from app.services.rules_service import RulesService
from app.services.logs_service import LogsService
from app.core.logger import logger
from datetime import datetime


class RateLimiter:
    """Rate limiting middleware"""
    
    @staticmethod
    async def check_rate_limit(request: Request, session: Session, client_ip: str) -> dict:
        """
        Check if IP has exceeded rate limits
        Returns dict with status and reason
        """
        # Get current rules
        rules = RulesService.get_current_rules(session)
        
        # Get or create IP activity
        ip_activity = IPService.get_or_create_ip(session, client_ip)
        
        # Check per-second limit
        if ip_activity.requests_last_second >= rules.max_req_per_sec:
            logger.warning(
                f"Rate limit exceeded (per second): {client_ip} - "
                f"{ip_activity.requests_last_second}/{rules.max_req_per_sec}"
            )
            
            # Block the IP
            IPService.block_ip(session, client_ip, rules.block_duration, "rate_limit_per_second")
            
            # Log the block
            LogsService.create_log(
                session,
                ip=client_ip,
                endpoint=str(request.url.path),
                status="blocked",
                reason="rate_limit_per_second_exceeded"
            )
            
            return {
                "allowed": False,
                "reason": "rate_limit_per_second_exceeded",
                "retry_after": rules.block_duration,
                "limit": rules.max_req_per_sec,
                "current": ip_activity.requests_last_second
            }
        
        # Check per-minute limit
        if ip_activity.requests_last_minute >= rules.max_req_per_min:
            logger.warning(
                f"Rate limit exceeded (per minute): {client_ip} - "
                f"{ip_activity.requests_last_minute}/{rules.max_req_per_min}"
            )
            
            # Block the IP
            IPService.block_ip(session, client_ip, rules.block_duration, "rate_limit_per_minute")
            
            # Log the block
            LogsService.create_log(
                session,
                ip=client_ip,
                endpoint=str(request.url.path),
                status="blocked",
                reason="rate_limit_per_minute_exceeded"
            )
            
            return {
                "allowed": False,
                "reason": "rate_limit_per_minute_exceeded",
                "retry_after": rules.block_duration,
                "limit": rules.max_req_per_min,
                "current": ip_activity.requests_last_minute
            }
        
        # Update counters
        IPService.update_request_count(session, client_ip)
        
        return {
            "allowed": True,
            "reason": "within_limits"
        }
