"""
Models package initialization.
This makes all models easily importable.
"""

# Import database configuration
from database import Base, Session, engine, init_db, get_session, reset_db

# Import models
from .client import Client
from .stylist import Stylist
# from .service import Service
# from .appointment import Appointment

# Make models available
__all__ = [
    'Base', 'Session', 'engine', 'init_db', 'get_session', 'reset_db',
    'Client', 'Stylist'
]