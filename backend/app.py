# app.py

import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv 
load_dotenv() 

# --- 1. Import extensions from the new extensions.py file ---
from extensions import db, jwt, cors

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def create_app():
    """
    Application factory function. This is the new standard for Flask apps.
    """
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # --- 2. All configuration is done inside the factory ---
    app.config['SECRET_KEY'] = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-production")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

    # --- MongoDB Configuration ---
    # Using an environment variable for the URI is highly recommended for security.
    # For now, this is fine for development.
    app.config['MONGODB_SETTINGS'] = {
        'host': os.environ.get('MONGODB_URI')
    }

    # --- 3. Initialize extensions using the app object ---
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # --- 4. Import and register the Blueprint ---
    # This ensures that the app is fully built before the routes are loaded.
    with app.app_context():
        from routes import bp as main_blueprint
        # The line below registers all the routes from routes.py with our app.
        app.register_blueprint(main_blueprint)

    # --- 5. Return the fully configured app instance ---
    return app


# --- 6. The main entry point for your application ---
# This line calls the factory to create the app.
# A WSGI server like Gunicorn will look for this 'app' variable.
app = create_app()
