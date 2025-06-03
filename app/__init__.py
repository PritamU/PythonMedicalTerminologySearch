from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
import os
# from app.routes import main
from flask import Flask
from app.extensions import db
from app.routes import main as main_bp

def create_app():
    print('create app started')
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.config.from_object("config.Config")

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        "DATABASE_URL", "postgresql://postgres:root@localhost/fhir"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        try:
            # from .models import MedicalConcept
            db.create_all()
            print("✅ Database initialized.")
        except Exception as e:
            print("❌ Error initializing database:", e)
    return app
