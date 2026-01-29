"""
Database configuration for SalonPro Manager.
This file sets up SQLAlchemy engine and session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Create the base class for all models
Base = declarative_base()

# Create engine - using SQLite for simplicity
DATABASE_URL = 'sqlite:///salonpro.db'
engine = create_engine(DATABASE_URL)

# Create Session class
Session = sessionmaker(bind=engine)

def get_session():
    """Get a new database session."""
    return Session()

def init_db():
    """Initialize the database by creating all tables."""
    # Import models here to ensure they're registered with Base
    from models.client import Client
    from models.stylist import Stylist
    from models.service import Service
    from models.appointment import Appointment
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print("Database tables created successfully!")
    return get_session()

def reset_db():
    """Reset the database (for testing)."""
    if os.path.exists('salonpro.db'):
        os.remove('salonpro.db')
        print("Old database removed.")
    
    return init_db()