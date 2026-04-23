from flask import Blueprint, render_template, jsonify
from app.models.patient import Patient
from app.models.therapy import TherapySession
from datetime import datetime, timedelta
from app import db
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Total patients
    total_patients = Patient.query.filter_by(is_active=True).count()

    # Get today's date
    today = datetime.utcnow().strftime('%Y-%m-%d')
    today_display = datetime.utcnow().strftime('%d %B %Y')

    # Upcoming sessions
    upcoming_sessions = TherapySession.query.filter_by(
        status='Scheduled'
    ).count()

    # Completed today
    completed_today = TherapySession.query.filter_by(
        status='Completed',
        session_date=today
    ).count()

    # Recent patients
    recent_patients = Patient.query.filter_by(is_active=True)\
                      .order_by(Patient.created_at.desc())\
                      .limit(5).all()

    # Upcoming sessions list
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

# ─── Chart Data APIs ──────────────────────────────

@main_bp.route('/api/dosha-chart')
def dosha_chart():
    """Returns dosha distribution data for pie chart"""
    results = db.session.query(
        Patient.dosha_type,
        func.count(Patient.id)
    ).filter(
        Patient.is_active == True,
        Patient.dosha_type != None
    ).group_by(Patient.dosha_type).all()

    labels = [r[0] for r in results]
    values = [r[1] for r in results]

    return jsonify({'labels': labels, 'values': values})

@main_bp.route('/api/therapy-chart')
def therapy_chart():
    """Returns therapy popularity data for bar chart"""
    results = db.session.query(
        TherapySession.therapy_name,
        func.count(TherapySession.id)
    ).group_by(TherapySession.therapy_name).all()

    labels = [r[0] for r in results]
    values = [r[1] for r in results]

    return jsonify({'labels': labels, 'values': values})

@main_bp.route('/api/patient-trend')
def patient_trend():
    """Returns patient registration trend for last 7 days"""
    labels = []
    values = []

    for i in range(6, -1, -1):
        date = datetime.utcnow() - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        label = date.strftime('%d %b')

        count = Patient.query.filter(
            func.date(Patient.created_at) == date_str
        ).count()

        labels.append(label)
        values.append(count)

    return jsonify({'labels': labels, 'values': values})

@main_bp.route('/api/status-chart')
def status_chart():
    """Returns session status distribution"""
    results = db.session.query(
        TherapySession.status,
        func.count(TherapySession.id)
    ).group_by(TherapySession.status).all()

    labels = [r[0] for r in results]
    values = [r[1] for r in results]

    return jsonify({'labels': labels, 'values': values})

@main_bp.route('/charts')
def charts():
    return render_template('charts.html')