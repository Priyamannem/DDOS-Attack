from fastapi import APIRouter, Request, Depends
from sqlmodel import Session
from api.database import get_db
from api.middleware.mitigation import DDoSMitigation
from datetime import datetime


router = APIRouter(tags=["Public"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DDoS Prevention System",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DDoS Prevention System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@router.get("/protected-resource")
async def protected_resource(
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Example protected endpoint
    This endpoint is protected by DDoS middleware
    """
    client_ip = DDoSMitigation.extract_client_ip(request)
    
    return {
        "message": "Access granted to protected resource",
        "your_ip": client_ip,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/test-endpoint")
async def test_endpoint(
    request: Request,
    data: dict = None,
    session: Session = Depends(get_db)
):
    """Test POST endpoint"""
    client_ip = DDoSMitigation.extract_client_ip(request)
    
    return {
        "message": "POST request successful",
        "your_ip": client_ip,
        "received_data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
