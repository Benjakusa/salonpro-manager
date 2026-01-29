"""
Service model for SalonPro Manager.
Represents services offered by the salon (haircut, color, treatment, etc.).
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False)  # Duration in minutes
    price = Column(Float, nullable=False)
    category = Column(String(50))  # e.g., "Haircut", "Color", "Treatment"
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    created_at = Column(DateTime, default=datetime.now)
    
    # One-to-many relationship with appointments
    appointments = relationship("Appointment", back_populates="service", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', price=${self.price}, duration={self.duration_minutes}min)>"
    
    # Property methods
    @property
    def formatted_price(self):
        return f"${self.price:.2f}"
    
    @property
    def formatted_duration(self):
        """Format duration as hours and minutes."""
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}min"
        return f"{minutes}min"
    
    @property
    def hourly_rate(self):
        """Calculate effective hourly rate."""
        if self.duration_minutes > 0:
            return (self.price / self.duration_minutes) * 60
        return 0
    
    # CLASS METHODS (ORM operations)
    
    @classmethod
    def create(cls, session, **kwargs):
        """Create a new service."""
        service = cls(**kwargs)
        session.add(service)
        session.commit()
        return service
    
    @classmethod
    def get_all(cls, session):
        """Get all services."""
        return session.query(cls).all()
    
    @classmethod
    def get_active(cls, session):
        """Get only active services."""
        return session.query(cls).filter_by(is_active=1).all()
    
    @classmethod
    def find_by_id(cls, session, service_id):
        """Find service by ID."""
        return session.query(cls).filter_by(id=service_id).first()
    
    @classmethod
    def find_by_name(cls, session, name):
        """Find services by name (partial match)."""
        return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()
    
    @classmethod
    def find_by_category(cls, session, category):
        """Find services by category."""
        return session.query(cls).filter_by(category=category).all()
    
    @classmethod
    def update(cls, session, service_id, **kwargs):
        """Update service information."""
        service = cls.find_by_id(session, service_id)
        if service:
            for key, value in kwargs.items():
                setattr(service, key, value)
            session.commit()
        return service
    
    @classmethod
    def delete(cls, session, service_id):
        """Deactivate a service."""
        service = cls.find_by_id(session, service_id)
        if service:
            service.is_active = 0  # Soft delete
            session.commit()
            return True
        return False
    
    # Instance method - FIXED: import inside method to avoid circular import
    def get_appointments(self, session):
        """Get all appointments for this service."""
        # Import here to avoid circular import
        from models.appointment import Appointment
        return session.query(Appointment).filter_by(service_id=self.id).all()