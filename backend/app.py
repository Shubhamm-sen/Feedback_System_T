import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
load_dotenv()

# --- 1. Import extensions from extensions.py ---
from extensions import db, jwt, cors
from flask_cors import CORS  # ✅ Important: CORS must be imported directly

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # --- 2. Application Config ---
    app.config['SECRET_KEY'] = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-production")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

    # --- 3. MongoDB Config ---
    app.config['MONGODB_SETTINGS'] = {
        'host': os.environ.get('MONGODB_URI')
    }

    # --- 4. Init Extensions ---
    db.init_app(app)
    jwt.init_app(app)

    # ✅ CORS fix: Allow frontend (Vercel) to access backend (Railway)
    CORS(app, origins=[
        "https://feedback-system-t.vercel.app",   # ✅ replace with your real Vercel domain
    ], supports_credentials=True)

    # --- 5. Register Blueprints ---
    with app.app_context():
        from routes import bp as main_blueprint
        app.register_blueprint(main_blueprint)

    return app


# --- 6. Create App ---
app = create_app()
