# extensions.py
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Create the extension instances here, but don't initialize them with the app yet.
db = MongoEngine()
jwt = JWTManager()
cors = CORS()