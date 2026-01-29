"""
Stylist model for SalonPro Manager.
Represents hair stylists/beauticians working at the salon.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Stylist(Base):
    __tablename__ = 'stylists'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    specialty = Column(String(100))  # e.g., "Coloring", "Men's cuts", "Extensions"
    hire_date = Column(DateTime, default=datetime.now)
    hourly_rate = Column(Float, default=25.0)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    
    # One-to-many relationship with appointments
    appointments = relationship("Appointment", back_populates="stylist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Stylist(id={self.id}, name='{self.first_name} {self.last_name}', specialty='{self.specialty}')>"
    
    # Property methods
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def formatted_phone(self):
        if len(self.phone) == 10:
            return f"({self.phone[:3]}) {self.phone[3:6]}-{self.phone[6:]}"
        return self.phone
    
    @property
    def experience_years(self):
        """Calculate years of experience since hire date."""
        if self.hire_date:
            delta = datetime.now() - self.hire_date
            return round(delta.days / 365.25, 1)
        return 0
    
    # CLASS METHODS (ORM operations)
    
    @classmethod
    def create(cls, session, **kwargs):
        """Create a new stylist."""
        stylist = cls(**kwargs)
        session.add(stylist)
        session.commit()
        return stylist
    
    @classmethod
    def get_all(cls, session):
        """Get all stylists."""
        return session.query(cls).all()
    
    @classmethod
    def get_active(cls, session):
        """Get only active stylists."""
        return session.query(cls).filter_by(is_active=1).all()
    
    @classmethod
    def find_by_id(cls, session, stylist_id):
        """Find stylist by ID."""
        return session.query(cls).filter_by(id=stylist_id).first()
    
    @classmethod
    def find_by_specialty(cls, session, specialty):
        """Find stylists by specialty."""
        return session.query(cls).filter_by(specialty=specialty).all()
    
    @classmethod
    def update(cls, session, stylist_id, **kwargs):
        """Update stylist information."""
        stylist = cls.find_by_id(session, stylist_id)
        if stylist:
            for key, value in kwargs.items():
                setattr(stylist, key, value)
            session.commit()
        return stylist
    
    @classmethod
    def delete(cls, session, stylist_id):
        """Delete (deactivate) a stylist."""
        stylist = cls.find_by_id(session, stylist_id)
        if stylist:
            stylist.is_active = 0  # Soft delete
            session.commit()
            return True
        return False
    
    # Instance method
    def get_appointments(self, session):
        """Get all appointments for this stylist."""
        from models.appointment import Appointment
        return session.query(Appointment).filter_by(stylist_id=self.id).all()
    
    def get_todays_appointments(self, session):
        """Get today's appointments for this stylist."""
        from models.appointment import Appointment
        from datetime import date
        today = date.today()
        return session.query(Appointment).filter_by(
            stylist_id=self.id,
            appointment_date=today
        ).all()