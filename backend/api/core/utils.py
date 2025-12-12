from datetime import datetime, timedelta
from typing import Optional
import random
import string


def generate_random_ip() -> str:
    """Generate a random IP address"""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def is_private_ip(ip: str) -> bool:
    """Check if IP is private/local"""
    private_ranges = [
        "127.", "10.", "192.168.", "172.16.", "172.17.", 
        "172.18.", "172.19.", "172.20.", "172.21.", "172.22.",
        "172.23.", "172.24.", "172.25.", "172.26.", "172.27.",
        "172.28.", "172.29.", "172.30.", "172.31."
    ]
    return any(ip.startswith(prefix) for prefix in private_ranges)


def calculate_block_until(duration_seconds: int) -> datetime:
    """Calculate when a block should expire"""
    return datetime.utcnow() + timedelta(seconds=duration_seconds)


def is_blocked_active(blocked_until: Optional[datetime]) -> bool:
    """Check if a block is still active"""
    if blocked_until is None:
        return False
    return datetime.utcnow() < blocked_until


def sanitize_string(text: str, max_length: int = 255) -> str:
    """Sanitize and truncate string input"""
    if not text:
        return ""
    # Remove control characters
    sanitized = ''.join(char for char in text if char.isprintable())
    return sanitized[:max_length]


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime for consistent display"""
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%d %H:%M:%S")
