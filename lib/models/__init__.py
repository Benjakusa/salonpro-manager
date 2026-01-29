"""
Models package initialization.
This makes all models easily importable.
"""

# We'll import database config differently to avoid circular imports
# Import models here so they can be accessed from models package
from .client import Client
from .stylist import Stylist
from .service import Service
from .appointment import Appointment

# Make models available
__all__ = [
    'Client', 'Stylist', 'Service', 'Appointment'
]