from fastapi import Request, Response
from fastapi.responses import JSONResponse
from sqlmodel import Session
from api.middleware.rate_limiter import RateLimiter
from api.middleware.anomaly_detector import AnomalyDetector
from api.middleware.ip_reputation import IPReputation
from api.services.logs_service import LogsService
from api.database import get_session
from api.core.logger import logger
from datetime import datetime


class DDoSMitigation:
    """
    Main DDoS mitigation middleware
    Coordinates all protection mechanisms
    """
    
    @staticmethod
    def extract_client_ip(request: Request) -> str:
        """Extract real client IP from request"""
        # Check for forwarded IP (proxy/load balancer)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # Get first IP in chain
            return forwarded.split(",")[0].strip()
        
        # Check for real IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # Fall back to direct client
        if request.client:
            return request.client.host
        
        return "unknown"
    
    @staticmethod
    async def process_request(request: Request, session: Session) -> dict:
        """
        Process incoming request through all security checks
        Returns dict with decision and metadata
        """
        client_ip = DDoSMitigation.extract_client_ip(request)
        endpoint = str(request.url.path)
        
        # Skip protection for health/admin endpoints (optional)
        if endpoint in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return {
                "allowed": True,
                "reason": "system_endpoint",
                "ip": client_ip
            }
        
        logger.info(f"Processing request: {client_ip} -> {endpoint}")
        
        # 1. Check IP reputation
        reputation = await IPReputation.check_reputation(session, client_ip)
        
        # If blacklisted, block immediately
        if reputation["is_blacklisted"]:
            LogsService.create_log(
                session,
                ip=client_ip,
                endpoint=endpoint,
                status="blocked",
                reason="blacklisted_ip"
            )
            return {
                "allowed": False,
                "reason": "blacklisted_ip",
                "ip": client_ip,
                "http_status": 403
            }
        
        # If blocked temporarily
        if reputation.get("is_blocked", False):
            LogsService.create_log(
                session,
                ip=client_ip,
                endpoint=endpoint,
                status="blocked",
                reason="temporarily_blocked"
            )
            return {
                "allowed": False,
                "reason": "temporarily_blocked",
                "ip": client_ip,
                "http_status": 429,
                "retry_after": 300
            }
        
        # If whitelisted, bypass all checks
        if reputation["bypass_checks"]:
            LogsService.create_log(
                session,
                ip=client_ip,
                endpoint=endpoint,
                status="allowed",
                reason="whitelisted_ip"
            )
            return {
                "allowed": True,
                "reason": "whitelisted_ip",
                "ip": client_ip
            }
        
        # 2. Check rate limits
        rate_limit_result = await RateLimiter.check_rate_limit(request, session, client_ip)
        
        if not rate_limit_result["allowed"]:
            return {
                "allowed": False,
                "reason": rate_limit_result["reason"],
                "ip": client_ip,
                "http_status": 429,
                "retry_after": rate_limit_result.get("retry_after", 300),
                "limit": rate_limit_result.get("limit"),
                "current": rate_limit_result.get("current")
            }
        
        # 3. Run anomaly detection
        anomaly_result = await AnomalyDetector.detect_anomalies(request, session, client_ip)
        
        if anomaly_result["auto_blocked"]:
            return {
                "allowed": False,
                "reason": "auto_blocked_anomaly",
                "ip": client_ip,
                "http_status": 429,
                "anomalies": anomaly_result["reasons"],
                "retry_after": 600
            }
        
        # Log allowed request
        status = "suspicious" if anomaly_result["is_suspicious"] else "allowed"
        LogsService.create_log(
            session,
            ip=client_ip,
            endpoint=endpoint,
            status=status,
            reason="normal_traffic" if status == "allowed" else ", ".join(anomaly_result["reasons"])
        )
        
        return {
            "allowed": True,
            "reason": "passed_all_checks",
            "ip": client_ip,
            "suspicious": anomaly_result["is_suspicious"],
            "anomalies": anomaly_result["reasons"] if anomaly_result["is_suspicious"] else []
        }
    
    @staticmethod
    def create_block_response(result: dict) -> JSONResponse:
        """Create standardized block response"""
        status_code = result.get("http_status", 429)
        
        response_body = {
            "status": "blocked",
            "ip": result["ip"],
            "reason": result["reason"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if "retry_after" in result:
            response_body["retry_after"] = result["retry_after"]
        
        if "limit" in result:
            response_body["limit"] = result["limit"]
            response_body["current"] = result["current"]
        
        if "anomalies" in result:
            response_body["anomalies"] = result["anomalies"]
        
        headers = {}
        if "retry_after" in result:
            headers["Retry-After"] = str(result["retry_after"])
        
        return JSONResponse(
            status_code=status_code,
            content=response_body,
            headers=headers
        )
