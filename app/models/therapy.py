from app import db
from datetime import datetime

class TherapySession(db.Model):
    __tablename__ = 'therapy_sessions'

    id = db.Column(db.Integer, primary_key=True)
    
    # Which patient is this for?
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), 
                          nullable=False)
    
    # Therapy details
    therapy_name = db.Column(db.String(100), nullable=False)
    therapist_name = db.Column(db.String(100), nullable=True)
    session_date = db.Column(db.String(20), nullable=False)
    session_time = db.Column(db.String(10), nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    
    # Status tracking
    status = db.Column(db.String(20), default='Scheduled')
    # Status options: Scheduled, In Progress, Completed, Cancelled
    
    # Additional
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # This connects session back to patient
    patient = db.relationship('Patient', backref='sessions')

    def __repr__(self):
        return f'<Session {self.therapy_name} for Patient {self.patient_id}>'
    