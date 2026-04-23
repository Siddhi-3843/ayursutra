from app import create_app, db
from app.models.patient import Patient
from app.models.therapy import TherapySession

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database is ready!")

if __name__ == '__main__':
    app.run(debug=False)