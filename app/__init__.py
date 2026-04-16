from flask import Flask, redirect, url_for
import os
from .config import Config
from .extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite:///"):
        db_path = db_uri.replace("sqlite:///", "", 1)
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from .auth.routes import auth_bp
    from .student.routes import student_bp
    from .librarian.routes import librarian_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(librarian_bp, url_prefix="/librarian")

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app