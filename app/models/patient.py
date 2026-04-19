from app import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'

    # Basic Information
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    date_of_birth = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_number = db.Column(db.String(15), nullable=True)

    # Visit Details
    reason_for_visit = db.Column(db.Text, nullable=True)
    department = db.Column(db.String(50), nullable=True)
    appointment_date = db.Column(db.String(20), nullable=True)

    # Medical History
    taken_treatment_before = db.Column(db.String(5), nullable=True)
    previous_diagnosis = db.Column(db.Text, nullable=True)
    previous_treatment_details = db.Column(db.Text, nullable=True)
    date_of_last_treatment = db.Column(db.String(20), nullable=True)

    # Ongoing Medicines
    taking_medicines = db.Column(db.String(5), nullable=True)
    medicine_name = db.Column(db.String(200), nullable=True)
    medicine_dosage = db.Column(db.String(100), nullable=True)
    medicine_duration = db.Column(db.String(100), nullable=True)

    # Allergies
    has_allergies = db.Column(db.String(5), nullable=True)
    allergy_type = db.Column(db.String(50), nullable=True)
    allergy_description = db.Column(db.Text, nullable=True)

    # Physical Details
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    bmi = db.Column(db.Float, nullable=True)

    # Lifestyle
    smoking = db.Column(db.String(5), nullable=True)
    alcohol = db.Column(db.String(5), nullable=True)
    exercise_level = db.Column(db.String(20), nullable=True)

    # Additional
    additional_notes = db.Column(db.Text, nullable=True)
    dosha_type = db.Column(db.String(20), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Patient {self.name}>'