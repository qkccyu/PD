# main.py
import os
from pathlib import Path

from flask import Flask, session, redirect, url_for, request
from jinja2 import DictLoader, ChoiceLoader
from dotenv import load_dotenv
from network_config import config

# DB
from extensions import db

# Models (so db.create_all() can see them)
import models  # noqa: F401

# --- Pages (blueprints + in-memory templates) ---
from pages.base_tpl import TEMPLATES as BASE_TPL

from pages.landing import bp as landing_page_bp, TEMPLATES as LANDING_TPL
from pages.dashboard import bp as dashboard_page_bp, TEMPLATES as DASHBOARD_TPL
from pages.patients import bp as patients_page_bp, TEMPLATES as PATIENTS_TPL
from pages.medications import bp as medications_page_bp, TEMPLATES as MEDICATIONS_TPL
from pages.scan import bp as scan_page_bp, TEMPLATES as SCAN_TPL
from pages.aboutus import bp as aboutus_page_bp, TEMPLATES as ABOUT_TPL
from pages.reports import bp as reports_page_bp, TEMPLATES as REPORTS_TPL
from pages.login import bp as login_page_bp, TEMPLATES as LOGIN_TPL

# --- APIs (blueprints) ---
from api.patients_api import bp as patients_api_bp
from api.medications_api import bp as medications_api_bp
from api.scans_api import bp as scans_api_bp


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__, static_folder="static")

    # ---------- Config ----------
    # Load configuration based on environment
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    # Set absolute path for database to avoid location issues
    db_path = os.path.abspath("mycoscan.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", f"sqlite:///{db_path}"
    )

    # Where uploaded scans are stored
    app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "uploads", "scans")
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    # ---------- DB ----------
    db.init_app(app)

    # ---------- Jinja templates (in-memory) ----------
    # Merge all TEMPLATES dicts from page modules
    templates = {}
    templates.update(BASE_TPL)
    templates.update(LANDING_TPL)
    templates.update(DASHBOARD_TPL)
    templates.update(PATIENTS_TPL)
    templates.update(MEDICATIONS_TPL)
    templates.update(SCAN_TPL)
    templates.update(ABOUT_TPL)
    templates.update(REPORTS_TPL)
    templates.update(LOGIN_TPL)

    # Prepend our DictLoader so these names resolve first
    app.jinja_loader = ChoiceLoader([DictLoader(templates), app.jinja_loader])

    # ---------- Register blueprints ----------
    # Pages
    app.register_blueprint(landing_page_bp)
    app.register_blueprint(dashboard_page_bp)
    app.register_blueprint(patients_page_bp)
    app.register_blueprint(medications_page_bp)
    app.register_blueprint(scan_page_bp)
    app.register_blueprint(aboutus_page_bp)
    app.register_blueprint(reports_page_bp)
    app.register_blueprint(login_page_bp)

    # APIs
    app.register_blueprint(patients_api_bp)
    app.register_blueprint(medications_api_bp)
    app.register_blueprint(scans_api_bp)

    # ---------- Authentication middleware ----------
    @app.before_request
    def require_login():
        # Public routes that don't require login
        public_routes = ['login_page.login', 'login_page.register', 'landing_page.landing']
        
        # Check if user is accessing a public route or static files
        if (request.endpoint in public_routes or 
            request.endpoint == 'static' or 
            request.path == '/' or
            request.path.startswith('/static/')):
            return
        
        # Check if user is logged in
        if 'user_id' not in session:
            print(f"DEBUG AUTH: No user_id in session for {request.endpoint} ({request.path})")
            print(f"DEBUG AUTH: Session keys: {list(session.keys())}")
            return redirect(url_for('login_page.login'))
        else:
            print(f"DEBUG AUTH: User {session.get('user_id')} accessing {request.endpoint}")

    # ---------- Create tables ----------
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    # Get network configuration
    from network_config import DevelopmentConfig
    config_obj = DevelopmentConfig()
    
    print(f"🚀 Starting MycoScan Server...")
    print(f"📡 Local access: http://localhost:{config_obj.PORT}")
    print(f"🌐 Network access: http://0.0.0.0:{config_obj.PORT}")
    print(f"🔐 Login credentials: admin / admin123")
    print(f"⚠️  Debug mode: {config_obj.DEBUG}")
    
    app.run(host=config_obj.HOST, port=config_obj.PORT, debug=config_obj.DEBUG)