from sqlmodel import Session
from api.services.traffic_service import TrafficService
from api.services.ip_service import IPService
from api.core.logger import logger


class IPReputation:
    """IP reputation checking"""
    
    @staticmethod
    async def check_reputation(session: Session, client_ip: str) -> dict:
        """
        Check IP against blacklist/whitelist
        Returns dict with reputation status
        """
        # Check whitelist first (trusted IPs bypass all checks)
        if TrafficService.is_whitelisted(session, client_ip):
            logger.info(f"Whitelisted IP accessed: {client_ip}")
            return {
                "is_whitelisted": True,
                "is_blacklisted": False,
                "bypass_checks": True,
                "reason": "whitelisted_ip"
            }
        
        # Check blacklist
        if TrafficService.is_blacklisted(session, client_ip):
            logger.warning(f"Blacklisted IP attempted access: {client_ip}")
            return {
                "is_whitelisted": False,
                "is_blacklisted": True,
                "bypass_checks": False,
                "reason": "blacklisted_ip"
            }
        
        # Check if IP is currently blocked
        if IPService.is_ip_blocked(session, client_ip):
            logger.warning(f"Blocked IP attempted access: {client_ip}")
            return {
                "is_whitelisted": False,
                "is_blacklisted": False,
                "is_blocked": True,
                "bypass_checks": False,
                "reason": "temporarily_blocked"
            }
        
        return {
            "is_whitelisted": False,
            "is_blacklisted": False,
            "is_blocked": False,
            "bypass_checks": False,
            "reason": "neutral"
        }
    
    @staticmethod
    def is_private_network(ip: str) -> bool:
        """Check if IP is from private network"""
        private_prefixes = [
            "10.", "172.16.", "172.17.", "172.18.", "172.19.",
            "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
            "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
            "172.30.", "172.31.", "192.168.", "127."
        ]
        return any(ip.startswith(prefix) for prefix in private_prefixes)
