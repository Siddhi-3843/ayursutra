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
    from app.routes.therapy import therapy_bp
    from app.routes.chatbot import chatbot_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(therapy_bp, url_prefix='/therapy')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

    return app