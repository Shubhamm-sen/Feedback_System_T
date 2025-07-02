import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from flask_cors import CORS
from extensions import jwt

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Logging setup
logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # ✅ App config
    app.config['SECRET_KEY'] = os.getenv("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "jwt-secret-change-in-production")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

    # ✅ Initialize JWT
    jwt.init_app(app)

    # ✅ Enable CORS
    CORS(app, origins=[
        "https://feedback-system-t.vercel.app"
    ], supports_credentials=True)

    # ✅ Register Blueprints
    with app.app_context():
        from routes import bp as main_blueprint
        app.register_blueprint(main_blueprint)

    return app

# ✅ WSGI entrypoint
app = create_app()

# ✅ Run locally
if __name__ == "__main__":
    app.run(debug=True)
