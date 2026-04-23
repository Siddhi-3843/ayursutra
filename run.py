from app import create_app, db
from app.models.patient import Patient
from app.models.therapy import TherapySession

app = create_app()

# This runs when gunicorn starts
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created!")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    app.run(debug=False)