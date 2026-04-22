from flask import Blueprint, render_template
from app.models.patient import Patient
from app.models.therapy import TherapySession
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Total patients
    total_patients = Patient.query.filter_by(is_active=True).count()

    # Get today's date as string
    today = datetime.utcnow().strftime('%Y-%m-%d')
    today_display = datetime.utcnow().strftime('%d %B %Y')

    # Upcoming sessions (Scheduled only)
    upcoming_sessions = TherapySession.query.filter_by(
        status='Scheduled'
    ).count()

    # Completed today
    completed_today = TherapySession.query.filter_by(
        status='Completed',
        session_date=today
    ).count()

    # Recent patients (last 5)
    recent_patients = Patient.query.filter_by(is_active=True)\
                      .order_by(Patient.created_at.desc())\
                      .limit(5).all()

    # Upcoming sessions list (next 5)
    upcoming_list = TherapySession.query.filter_by(
        status='Scheduled'
    ).order_by(TherapySession.session_date.asc())\
     .limit(5).all()

    return render_template('index.html',
        total_patients=total_patients,
        upcoming_sessions=upcoming_sessions,
        completed_today=completed_today,
        recent_patients=recent_patients,
        upcoming_list=upcoming_list,
        today=today_display
    )