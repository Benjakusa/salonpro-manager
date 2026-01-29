"""
Database configuration for SalonPro Manager.
This file sets up SQLAlchemy engine and session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create the base class for all models
Base = declarative_base()

# Create engine - using SQLite for simplicity
engine = create_engine('sqlite:///salonpro.db')

# Create Session class
Session = sessionmaker(bind=engine)

def init_db():
    """Initialize the database by creating all tables."""
    # Import models here to ensure they're registered with Base
    from models.client import Client
    from models.stylist import Stylist
    # We'll add Service and Appointment later
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print("Database tables created successfully!")
    return Session()
