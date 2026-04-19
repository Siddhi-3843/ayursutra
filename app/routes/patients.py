from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.patient import Patient

patients_bp = Blueprint('patients', __name__)

# ─── List all patients ───────────────────────────
@patients_bp.route('/')
def list_patients():
    patients = Patient.query.filter_by(is_active=True).all()
    return render_template('patients.html', patients=patients)

# ─── Add new patient ─────────────────────────────
@patients_bp.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':

        # Calculate BMI automatically
        height = request.form.get('height')
        weight = request.form.get('weight')
        bmi = None
        if height and weight:
            h = float(height) / 100  # convert cm to meters
            w = float(weight)
            bmi = round(w / (h * h), 2)

        # Create new patient object
        patient = Patient(
            # Basic Info
            name=request.form.get('name'),
            age=request.form.get('age'),
            date_of_birth=request.form.get('date_of_birth'),
            gender=request.form.get('gender'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            emergency_contact_name=request.form.get('emergency_contact_name'),
            emergency_contact_number=request.form.get('emergency_contact_number'),

            # Visit Details
            reason_for_visit=request.form.get('reason_for_visit'),
            department=request.form.get('department'),
            appointment_date=request.form.get('appointment_date'),

            # Medical History
            taken_treatment_before=request.form.get('taken_treatment_before'),
            previous_diagnosis=request.form.get('previous_diagnosis'),
            previous_treatment_details=request.form.get('previous_treatment_details'),
            date_of_last_treatment=request.form.get('date_of_last_treatment'),

            # Medicines
            taking_medicines=request.form.get('taking_medicines'),
            medicine_name=request.form.get('medicine_name'),
            medicine_dosage=request.form.get('medicine_dosage'),
            medicine_duration=request.form.get('medicine_duration'),

            # Allergies
            has_allergies=request.form.get('has_allergies'),
            allergy_type=request.form.get('allergy_type'),
            allergy_description=request.form.get('allergy_description'),

            # Physical
            height=height,
            weight=weight,
            bmi=bmi,

            # Lifestyle
            smoking=request.form.get('smoking'),
            alcohol=request.form.get('alcohol'),
            exercise_level=request.form.get('exercise_level'),
            dosha_type=request.form.get('dosha_type'),

            # Additional
            additional_notes=request.form.get('additional_notes'),
        )

        db.session.add(patient)
        db.session.commit()
        flash(f'Patient {patient.name} registered successfully! 🌿', 'success')
        return redirect(url_for('patients.list_patients'))

    return render_template('add_patient.html')

# ─── View single patient ──────────────────────────
@patients_bp.route('/<int:patient_id>')
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('view_patient.html', patient=patient)