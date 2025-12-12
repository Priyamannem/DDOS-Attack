"""
Database initialization script
Run this to set up the database with initial data
"""
from api.database import create_db_and_tables, get_session
from api.services.rules_service import RulesService
from api.services.traffic_service import TrafficService
from api.core.config import settings
from api.core.logger import logger


def initialize_database():
    """Initialize database with tables and default data"""
    logger.info("Initializing database...")
    
    # Create all tables
    create_db_and_tables()
    logger.info("✓ Database tables created")
    
    # Create default rules
    with get_session() as session:
        rules = RulesService.get_current_rules(session)
        logger.info(f"✓ Default rules created: {rules.dict()}")
        
        # Add localhost to whitelist
        TrafficService.add_to_whitelist(session, "127.0.0.1")
        logger.info("✓ Added localhost to whitelist")
        
        # Add example blacklist entry
        TrafficService.add_to_blacklist(session, "0.0.0.0", "example_blocked_ip")
        logger.info("✓ Added example blacklist entry")
    
    logger.info("✅ Database initialization completed successfully!")


if __name__ == "__main__":
    initialize_database()
