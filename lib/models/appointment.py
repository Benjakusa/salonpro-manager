"""
Appointment model for SalonPro Manager.
Represents bookings linking clients, stylists, and services.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint, Text
from sqlalchemy.orm import relationship, validates
from datetime import datetime, time, timedelta
from database import Base

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    
    # Foreign keys
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    stylist_id = Column(Integer, ForeignKey('stylists.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    
    # Appointment details
    appointment_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    status = Column(String(20), default='scheduled')
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="appointments")
    stylist = relationship("Stylist", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    
    # Check constraint for status
    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled', 'no-show')",
            name='check_appointment_status'
        ),
    )
    
    def __repr__(self):
        return f"<Appointment(id={self.id}, client={self.client_id}, stylist={self.stylist_id}, date={self.appointment_date.date()})>"
    
    # Property methods
    @property
    def formatted_date(self):
        """Format appointment date nicely."""
        return self.appointment_date.strftime("%A, %B %d, %Y at %I:%M %p")
    
    @property
    def time_only(self):
        """Get just the time portion."""
        return self.appointment_date.strftime("%I:%M %p")
    
    @property
    def date_only(self):
        """Get just the date portion."""
        return self.appointment_date.strftime("%Y-%m-%d")
    
    @property
    def end_time(self):
        """Calculate appointment end time."""
        return self.appointment_date + timedelta(minutes=self.duration_minutes)
    
    @property
    def is_past(self):
        """Check if appointment is in the past."""
        return self.appointment_date < datetime.now()
    
    @property
    def is_today(self):
        """Check if appointment is today."""
        return self.appointment_date.date() == datetime.now().date()
    
    @property
    def is_upcoming(self):
        """Check if appointment is upcoming (not past)."""
        return not self.is_past and self.status == 'scheduled'
    
    # Validation method
    @validates('status')
    def validate_status(self, key, status):
        """Validate status value."""
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        return status
    
    # CLASS METHODS (ORM operations)
    
    @classmethod
    def create(cls, session, **kwargs):
        """Create a new appointment with validation."""
        # Check for scheduling conflicts
        if cls.has_conflict(session, 
                           kwargs['stylist_id'], 
                           kwargs['appointment_date'], 
                           kwargs.get('duration_minutes', 60)):
            raise ValueError("Scheduling conflict! Stylist is already booked at this time.")
        
        appointment = cls(**kwargs)
        session.add(appointment)
        session.commit()
        return appointment
    
    @classmethod
    def get_all(cls, session):
        """Get all appointments."""
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, appointment_id):
        """Find appointment by ID."""
        return session.query(cls).filter_by(id=appointment_id).first()
    
    @classmethod
    def find_by_client(cls, session, client_id):
        """Find all appointments for a client."""
        return session.query(cls).filter_by(client_id=client_id).all()
    
    @classmethod
    def find_by_stylist(cls, session, stylist_id):
        """Find all appointments for a stylist."""
        return session.query(cls).filter_by(stylist_id=stylist_id).all()
    
    @classmethod
    def find_by_date(cls, session, date):
        """Find appointments on a specific date."""
        start_date = datetime.combine(date, time.min)
        end_date = datetime.combine(date, time.max)
        
        return session.query(cls).filter(
            cls.appointment_date >= start_date,
            cls.appointment_date <= end_date
        ).all()
    
    @classmethod
    def find_upcoming(cls, session):
        """Find all upcoming appointments."""
        return session.query(cls).filter(
            cls.appointment_date >= datetime.now(),
            cls.status == 'scheduled'
        ).all()
    
    @classmethod
    def update(cls, session, appointment_id, **kwargs):
        """Update appointment information."""
        appointment = cls.find_by_id(session, appointment_id)
        if appointment:
            # Check for conflicts if time is being changed
            if 'appointment_date' in kwargs or 'duration_minutes' in kwargs:
                new_time = kwargs.get('appointment_date', appointment.appointment_date)
                new_duration = kwargs.get('duration_minutes', appointment.duration_minutes)
                
                if cls.has_conflict(session, 
                                  appointment.stylist_id, 
                                  new_time, 
                                  new_duration,
                                  exclude_id=appointment_id):
                    raise ValueError("Scheduling conflict! Stylist is already booked at this time.")
            
            for key, value in kwargs.items():
                setattr(appointment, key, value)
            session.commit()
        return appointment
    
    @classmethod
    def delete(cls, session, appointment_id):
        """Delete an appointment."""
        appointment = cls.find_by_id(session, appointment_id)
        if appointment:
            session.delete(appointment)
            session.commit()
            return True
        return False
    
    @classmethod
    def cancel(cls, session, appointment_id):
        """Cancel an appointment (soft delete)."""
        appointment = cls.find_by_id(session, appointment_id)
        if appointment:
            appointment.status = 'cancelled'
            session.commit()
            return True
        return False
    
    @classmethod
    def has_conflict(cls, session, stylist_id, start_time, duration_minutes=60, exclude_id=None):
        """Check if a stylist has a scheduling conflict."""
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        # Get all scheduled appointments for this stylist
        appointments = session.query(cls).filter(
            cls.stylist_id == stylist_id,
            cls.status == 'scheduled'
        ).all()
        
        if exclude_id:
            appointments = [app for app in appointments if app.id != exclude_id]
        
        # Check each appointment for overlap
        for appointment in appointments:
            appointment_end = appointment.appointment_date + timedelta(minutes=appointment.duration_minutes)
            
            # Check if time ranges overlap
            if (start_time < appointment_end) and (end_time > appointment.appointment_date):
                return True
        
        return False
    
    @classmethod
    def get_daily_revenue(cls, session, date):
        """Calculate total revenue for a specific day."""
        appointments = cls.find_by_date(session, date)
        return sum(app.total_price for app in appointments if app.status == 'completed')
    
    # Instance method
    def get_service_details(self):
        """Get service name and price."""
        if self.service:
            return f"{self.service.name} - ${self.service.price:.2f}"
        return "Service details not available"