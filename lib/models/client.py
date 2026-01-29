"""
Client model for SalonPro Manager.
Represents salon customers with their contact information.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.now)
    notes = Column(Text)  # Hair type, allergies, preferences, etc.
    
    # One-to-many relationship with appointments
    appointments = relationship("Appointment", back_populates="client", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.first_name} {self.last_name}', phone='{self.phone}')>"
    
    # Property method for full name
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    # Property method for validating email
    @property
    def email_is_valid(self):
        if not self.email:
            return False
        return '@' in self.email and '.' in self.email
    
    # Property method for phone formatting
    @property
    def formatted_phone(self):
        if len(self.phone) == 10:
            return f"({self.phone[:3]}) {self.phone[3:6]}-{self.phone[6:]}"
        return self.phone
    
    # CLASS METHODS (ORM operations)
    
    @classmethod
    def create(cls, session, **kwargs):
        """Create a new client."""
        client = cls(**kwargs)
        session.add(client)
        session.commit()
        return client
    
    @classmethod
    def get_all(cls, session):
        """Get all clients."""
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, client_id):
        """Find client by ID."""
        return session.query(cls).filter_by(id=client_id).first()
    
    @classmethod
    def find_by_phone(cls, session, phone):
        """Find client by phone number."""
        return session.query(cls).filter_by(phone=phone).first()
    
    @classmethod
    def find_by_name(cls, session, name):
        """Find clients by name (partial match)."""
        return session.query(cls).filter(
            (cls.first_name.ilike(f"%{name}%")) | 
            (cls.last_name.ilike(f"%{name}%"))
        ).all()
    
    @classmethod
    def update(cls, session, client_id, **kwargs):
        """Update client information."""
        client = cls.find_by_id(session, client_id)
        if client:
            for key, value in kwargs.items():
                setattr(client, key, value)
            session.commit()
        return client
    
    @classmethod
    def delete(cls, session, client_id):
        """Delete a client."""
        client = cls.find_by_id(session, client_id)
        if client:
            session.delete(client)
            session.commit()
            return True
        return False
    
    # Instance method
    def get_appointments(self, session):
        """Get all appointments for this client."""
        from models.appointment import Appointment
        return session.query(Appointment).filter_by(client_id=self.id).all()