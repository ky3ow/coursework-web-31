from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed password
    role = db.Column(db.String(20), nullable=False, default='volunteer')

    created_events = db.relationship('Event', back_populates='creator', lazy='dynamic')
    event_registrations = db.relationship('Registration', back_populates='user', lazy='dynamic')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', back_populates='created_events')
    
    date = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(300), nullable=True)
    
    registrations = db.relationship('Registration', back_populates='event', lazy='dynamic')

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    status = db.Column(db.String(20), default="pending")
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='event_registrations')
    event = db.relationship('Event', back_populates='registrations')
    
    # Unique constraint to prevent duplicate registrations
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='_user_event_uc'),)
