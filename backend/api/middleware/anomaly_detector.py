from fastapi import Request
from sqlmodel import Session, select
from api.services.rules_service import RulesService
from api.services.logs_service import LogsService
from api.services.ip_service import IPService
from api.models.ip_activity import IPActivity
from api.core.logger import logger
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict


class AnomalyDetector:
    """Detect anomalous traffic patterns"""
    
    # In-memory tracking for anomaly detection
    endpoint_access_tracker: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    global_request_tracker: list = []
    
    @staticmethod
    async def detect_anomalies(request: Request, session: Session, client_ip: str) -> dict:
        """
        Detect various anomaly patterns
        Returns dict with is_suspicious flag and reasons
        """
        rules = RulesService.get_current_rules(session)
        suspicious_reasons = []
        is_suspicious = False
        
        # 1. Check global traffic spike
        current_time = datetime.utcnow()
        AnomalyDetector.global_request_tracker.append(current_time)
        
        # Clean old entries (keep last minute)
        cutoff_time = current_time - timedelta(minutes=1)
        AnomalyDetector.global_request_tracker = [
            t for t in AnomalyDetector.global_request_tracker if t > cutoff_time
        ]
        
        global_rpm = len(AnomalyDetector.global_request_tracker)
        
        if global_rpm > rules.anomaly_threshold:
            suspicious_reasons.append(f"global_traffic_spike_{global_rpm}_rpm")
            is_suspicious = True
            logger.warning(f"Global traffic spike detected: {global_rpm} requests/minute")
        
        # 2. Check repeated endpoint access
        endpoint = str(request.url.path)
        AnomalyDetector.endpoint_access_tracker[client_ip][endpoint] += 1
        
        endpoint_count = AnomalyDetector.endpoint_access_tracker[client_ip][endpoint]
        if endpoint_count > 50:  # Same endpoint 50+ times
            suspicious_reasons.append(f"repeated_endpoint_access_{endpoint_count}")
            is_suspicious = True
            logger.warning(f"Repeated endpoint access: {client_ip} -> {endpoint} ({endpoint_count} times)")
        
        # 3. Check IP activity patterns
        ip_activity = IPService.get_or_create_ip(session, client_ip)
        
        # High request velocity
        if ip_activity.requests_last_second > 5:
            suspicious_reasons.append(f"high_velocity_{ip_activity.requests_last_second}_rps")
            is_suspicious = True
        
        # 4. Check for burst pattern (many requests in short time)
        if ip_activity.requests_last_minute > rules.max_req_per_min * 0.8:
            suspicious_reasons.append("approaching_rate_limit")
            is_suspicious = True
        
        # Log suspicious activity
        if is_suspicious:
            LogsService.create_log(
                session,
                ip=client_ip,
                endpoint=endpoint,
                status="suspicious",
                reason=", ".join(suspicious_reasons)
            )
            
            # Auto-block if too many anomalies
            if len(suspicious_reasons) >= 3:
                logger.error(f"Auto-blocking {client_ip} due to multiple anomalies: {suspicious_reasons}")
                IPService.block_ip(session, client_ip, rules.block_duration * 2, "multiple_anomalies")
                
                return {
                    "is_suspicious": True,
                    "auto_blocked": True,
                    "reasons": suspicious_reasons
                }
        
        return {
            "is_suspicious": is_suspicious,
            "auto_blocked": False,
            "reasons": suspicious_reasons
        }
    
    @staticmethod
    def reset_trackers():
        """Reset in-memory tracking (for testing/cleanup)"""
        AnomalyDetector.endpoint_access_tracker.clear()
        AnomalyDetector.global_request_tracker.clear()
