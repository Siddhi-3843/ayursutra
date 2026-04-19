from flask import Blueprint, render_template
from app.models.patient import Patient
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch real data from database
    total_patients = Patient.query.filter_by(is_active=True).count()
    
    # Get 5 most recently registered patients
    recent_patients = Patient.query.filter_by(is_active=True)\
                      .order_by(Patient.created_at.desc())\
                      .limit(5).all()
    
    # Get today's date
    today = datetime.utcnow().strftime('%d %B %Y')

    return render_template('index.html',
        total_patients=total_patients,
        recent_patients=recent_patients,
        today=today
    )