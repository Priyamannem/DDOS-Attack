from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from api.database import get_db
from api.services.logs_service import LogsService
from api.services.ip_service import IPService
from api.core.utils import generate_random_ip
from api.core.logger import logger
import random
from datetime import datetime


router = APIRouter(prefix="/simulate", tags=["Simulation"])


@router.get("/high-traffic")
async def simulate_high_traffic(
    count: int = Query(default=5000, ge=1, le=100000),
    ip: str = Query(default="random", description="Use 'random' for random IPs or 'auto' for single IP"),
    session: Session = Depends(get_db)
):
    """
    Simulate high traffic for testing
    WARNING: This will generate database entries
    """
    logger.warning(f"Starting traffic simulation: {count} requests")
    
    simulated_ips = []
    endpoints = [
        "/api/data", "/api/users", "/api/products",
        "/api/orders", "/api/search", "/api/login",
        "/api/dashboard", "/api/settings"
    ]
    
    # Determine IP mode
    if ip.lower() == "auto":
        source_ip = generate_random_ip()
        simulated_ips.append(source_ip)
    
    for i in range(count):
        # Generate IP
        if ip.lower() == "random":
            source_ip = generate_random_ip()
        elif ip.lower() == "auto":
            # Use same IP
            pass
        else:
            # Use provided IP
            source_ip = ip
        
        # Random endpoint
        endpoint = random.choice(endpoints)
        
        # Update IP activity
        try:
            IPService.update_request_count(session, source_ip)
            
            # Log every 100th request to avoid database overload
            if i % 100 == 0:
                LogsService.create_log(
                    session,
                    ip=source_ip,
                    endpoint=endpoint,
                    status="allowed",
                    reason=f"simulation_batch_{i//100}"
                )
        except Exception as e:
            logger.error(f"Error in simulation: {e}")
            continue
    
    logger.warning(f"Traffic simulation completed: {count} requests")
    
    return {
        "success": True,
        "message": f"Simulated {count} requests",
        "mode": ip,
        "simulated_ips": list(set(simulated_ips)) if ip.lower() == "random" else [source_ip],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ddos-attack")
async def simulate_ddos_attack(
    target_ips: int = Query(default=100, ge=1, le=1000),
    requests_per_ip: int = Query(default=500, ge=1, le=10000),
    session: Session = Depends(get_db)
):
    """
    Simulate a distributed DDoS attack from multiple IPs
    This will trigger rate limiting and anomaly detection
    """
    logger.warning(f"Starting DDoS simulation: {target_ips} IPs x {requests_per_ip} requests")
    
    total_requests = 0
    blocked_count = 0
    attacking_ips = []
    
    for _ in range(target_ips):
        attacker_ip = generate_random_ip()
        attacking_ips.append(attacker_ip)
        
        for req_num in range(requests_per_ip):
            try:
                ip_activity = IPService.update_request_count(session, attacker_ip)
                total_requests += 1
                
                # Check if got blocked
                if ip_activity.is_blocked:
                    blocked_count += 1
                    break  # Move to next IP
                
            except Exception as e:
                logger.error(f"Error in DDoS simulation: {e}")
                continue
    
    logger.warning(f"DDoS simulation completed: {total_requests} total requests, {blocked_count} IPs blocked")
    
    return {
        "success": True,
        "message": f"DDoS simulation completed",
        "total_requests": total_requests,
        "attacking_ips_count": target_ips,
        "blocked_count": blocked_count,
        "sample_attacking_ips": attacking_ips[:10],
        "timestamp": datetime.utcnow().isoformat()
    }
