from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.main import main_bp
    from app.routes.patients import patients_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(patients_bp, url_prefix='/patients')

    return app