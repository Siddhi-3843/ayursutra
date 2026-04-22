from app import create_app, db
from app.models.patient import Patient
from app.models.therapy import TherapySession

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database is ready!")
    app.run(debug=True)