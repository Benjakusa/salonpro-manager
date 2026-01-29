"""
Models package initialization.
Import all models here to make them available.
"""

# Import database configuration
from database import Base, Session, engine

# Import all model classes here (we'll create them next)
# from .client import Client
# from .stylist import Stylist
# from .service import Service
# from .appointment import Appointment

def get_session():
    """Get a new database session."""
    return Session()

# For now, just export the Base and Session
__all__ = ['Base', 'Session', 'engine', 'get_session']
