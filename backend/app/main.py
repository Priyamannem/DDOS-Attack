from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import logger
from app.database import create_db_and_tables, get_session
from app.middleware.mitigation import DDoSMitigation
from app.routers import admin, simulate, public


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting DDoS Prevention System...")
    logger.info(f"Creating database tables...")
    create_db_and_tables()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down DDoS Prevention System...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Advanced DDoS Attack Prevention and Monitoring System",
    lifespan=lifespan
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DDoS Protection Middleware
@app.middleware("http")
async def ddos_protection_middleware(request: Request, call_next):
    """
    Global DDoS protection middleware
    Applied to all requests except documentation
    """
    # Skip middleware for excluded paths
    excluded_paths = ["/docs", "/redoc", "/openapi.json"]
    if request.url.path in excluded_paths:
        return await call_next(request)
    
    # Process request through DDoS mitigation
    with get_session() as session:
        result = await DDoSMitigation.process_request(request, session)
        
        # If blocked, return error response
        if not result["allowed"]:
            return DDoSMitigation.create_block_response(result)
        
        # If suspicious, add warning header
        response = await call_next(request)
        
        if result.get("suspicious", False):
            response.headers["X-Security-Warning"] = "Suspicious activity detected"
            response.headers["X-Anomalies"] = ", ".join(result.get("anomalies", []))
        
        return response


# Include routers
app.include_router(public.router)
app.include_router(admin.router)
app.include_router(simulate.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
