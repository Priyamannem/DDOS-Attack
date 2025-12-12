from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.services.rules_service import RulesService
from app.services.logs_service import LogsService
from app.services.stats_service import StatsService
from app.services.ip_service import IPService
from app.services.traffic_service import TrafficService
from app.models.rules import Rules
from pydantic import BaseModel
from typing import Optional, List


router = APIRouter(prefix="/admin", tags=["Admin"])


# Pydantic models for requests
class UpdateRulesRequest(BaseModel):
    max_req_per_sec: Optional[int] = None
    max_req_per_min: Optional[int] = None
    block_duration: Optional[int] = None
    anomaly_threshold: Optional[int] = None


class AddBlacklistRequest(BaseModel):
    ip: str
    reason: str


class AddWhitelistRequest(BaseModel):
    ip: str


class RemoveIPRequest(BaseModel):
    ip: str


class UnblockIPRequest(BaseModel):
    ip: str


# Routes
@router.get("/rules")
async def get_rules(session: Session = Depends(get_db)):
    """Get current protection rules"""
    rules = RulesService.get_current_rules(session)
    return {
        "success": True,
        "rules": rules
    }


@router.post("/update_rules")
async def update_rules(
    request: UpdateRulesRequest,
    session: Session = Depends(get_db)
):
    """Update protection rules"""
    updated_rules = RulesService.update_rules(
        session,
        max_req_per_sec=request.max_req_per_sec,
        max_req_per_min=request.max_req_per_min,
        block_duration=request.block_duration,
        anomaly_threshold=request.anomaly_threshold
    )
    
    return {
        "success": True,
        "message": "Rules updated successfully",
        "rules": updated_rules
    }


@router.get("/logs/recent")
async def get_recent_logs(
    limit: int = 200,
    session: Session = Depends(get_db)
):
    """Get recent log entries"""
    logs = LogsService.get_recent_logs(session, limit=limit)
    return {
        "success": True,
        "count": len(logs),
        "logs": logs
    }


@router.get("/traffic/stats")
async def get_traffic_stats(
    minutes: int = 60,
    session: Session = Depends(get_db)
):
    """Get traffic statistics"""
    stats = StatsService.get_recent_stats(session, minutes=minutes)
    latest = StatsService.get_latest_stats(session)
    
    return {
        "success": True,
        "latest": latest,
        "history": stats,
        "count": len(stats)
    }


@router.get("/ip/{ip}")
async def get_ip_details(
    ip: str,
    session: Session = Depends(get_db)
):
    """Get full activity details for a specific IP"""
    ip_activity = IPService.get_or_create_ip(session, ip)
    logs = LogsService.get_logs_by_ip(session, ip, limit=100)
    is_blacklisted = TrafficService.is_blacklisted(session, ip)
    is_whitelisted = TrafficService.is_whitelisted(session, ip)
    
    return {
        "success": True,
        "ip": ip,
        "activity": ip_activity,
        "logs": logs,
        "is_blacklisted": is_blacklisted,
        "is_whitelisted": is_whitelisted
    }


@router.post("/add_to_blacklist")
async def add_to_blacklist(
    request: AddBlacklistRequest,
    session: Session = Depends(get_db)
):
    """Add IP to blacklist"""
    entry = TrafficService.add_to_blacklist(session, request.ip, request.reason)
    
    # Also block the IP immediately
    IPService.block_ip(session, request.ip, 31536000, "blacklisted")  # 1 year
    
    return {
        "success": True,
        "message": f"IP {request.ip} added to blacklist",
        "entry": entry
    }


@router.post("/add_to_whitelist")
async def add_to_whitelist(
    request: AddWhitelistRequest,
    session: Session = Depends(get_db)
):
    """Add IP to whitelist"""
    entry = TrafficService.add_to_whitelist(session, request.ip)
    
    # Unblock if currently blocked
    IPService.unblock_ip(session, request.ip)
    
    return {
        "success": True,
        "message": f"IP {request.ip} added to whitelist",
        "entry": entry
    }


@router.post("/remove_ip")
async def remove_ip(
    request: RemoveIPRequest,
    session: Session = Depends(get_db)
):
    """Remove IP from blacklist or whitelist"""
    removed_from_blacklist = TrafficService.remove_from_blacklist(session, request.ip)
    removed_from_whitelist = TrafficService.remove_from_whitelist(session, request.ip)
    
    if removed_from_blacklist or removed_from_whitelist:
        source = "blacklist" if removed_from_blacklist else "whitelist"
        return {
            "success": True,
            "message": f"IP {request.ip} removed from {source}"
        }
    else:
        raise HTTPException(status_code=404, detail=f"IP {request.ip} not found in lists")


@router.post("/unblock_ip")
async def unblock_ip(
    request: UnblockIPRequest,
    session: Session = Depends(get_db)
):
    """Unblock a temporarily blocked IP"""
    result = IPService.unblock_ip(session, request.ip)
    
    if result:
        return {
            "success": True,
            "message": f"IP {request.ip} unblocked successfully"
        }
    else:
        raise HTTPException(status_code=404, detail=f"IP {request.ip} not found")


@router.get("/blocked_ips")
async def get_blocked_ips(session: Session = Depends(get_db)):
    """Get all currently blocked IPs"""
    blocked = IPService.get_blocked_ips(session)
    
    return {
        "success": True,
        "count": len(blocked),
        "blocked_ips": blocked
    }


@router.get("/blacklist")
async def get_blacklist(session: Session = Depends(get_db)):
    """Get all blacklisted IPs"""
    blacklist = TrafficService.get_all_blacklisted(session)
    
    return {
        "success": True,
        "count": len(blacklist),
        "blacklist": blacklist
    }


@router.get("/whitelist")
async def get_whitelist(session: Session = Depends(get_db)):
    """Get all whitelisted IPs"""
    whitelist = TrafficService.get_all_whitelisted(session)
    
    return {
        "success": True,
        "count": len(whitelist),
        "whitelist": whitelist
    }
