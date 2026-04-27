from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.therapy import TherapySession
from app.models.patient import Patient

therapy_bp = Blueprint('therapy', __name__)

# ─── List all sessions ────────────────────────────
@therapy_bp.route('/')
def list_sessions():
    sessions = TherapySession.query\
                .order_by(TherapySession.session_date.asc())\
                .all()
    return render_template('therapy/list.html', sessions=sessions)

# ─── Schedule new session ─────────────────────────
@therapy_bp.route('/add', methods=['GET', 'POST'])
def add_session():
    patients = Patient.query.filter_by(is_active=True).all()
    
    if request.method == 'POST':
        session = TherapySession(
            patient_id=request.form.get('patient_id'),
            therapy_name=request.form.get('therapy_name'),
            therapist_name=request.form.get('therapist_name'),
            session_date=request.form.get('session_date'),
            session_time=request.form.get('session_time'),
            duration_minutes=request.form.get('duration_minutes'),
            notes=request.form.get('notes'),
            status='Scheduled'
        )
        db.session.add(session)
        db.session.commit()
        flash(f'Session scheduled successfully! 📅', 'success')
        return redirect(url_for('therapy.list_sessions'))
    
    return render_template('therapy/add.html', patients=patients)

# ─── Update session status ────────────────────────
@therapy_bp.route('/update-status/<int:session_id>', methods=['POST'])
def update_status(session_id):
    session = TherapySession.query.get_or_404(session_id)
    new_status = request.form.get('status')
    session.status = new_status
    db.session.commit()
    flash(f'Session status updated to {new_status}! ✅', 'success')
    return redirect(url_for('therapy.list_sessions'))

# ─── Edit therapy session ─────────────────────────
@therapy_bp.route('/edit/<int:session_id>', methods=['GET', 'POST'])
def edit_session(session_id):
    session = TherapySession.query.get_or_404(session_id)
    patients = Patient.query.filter_by(is_active=True).all()

    if request.method == 'POST':
        session.patient_id = request.form.get('patient_id')
        session.therapy_name = request.form.get('therapy_name')
        session.therapist_name = request.form.get('therapist_name')
        session.session_date = request.form.get('session_date')
        session.session_time = request.form.get('session_time')
        session.duration_minutes = request.form.get('duration_minutes')
        session.notes = request.form.get('notes')
        session.status = request.form.get('status')

        db.session.commit()
        flash('Session updated successfully! ✅', 'success')
        return redirect(url_for('therapy.list_sessions'))

    return render_template('therapy/edit.html',
                           session=session, patients=patients)

# ─── Delete therapy session ───────────────────────
@therapy_bp.route('/delete/<int:session_id>', methods=['POST'])
def delete_session(session_id):
    session = TherapySession.query.get_or_404(session_id)
    db.session.delete(session)
    db.session.commit()
    flash('Session deleted successfully! 🗑️', 'success')
    return redirect(url_for('therapy.list_sessions'))