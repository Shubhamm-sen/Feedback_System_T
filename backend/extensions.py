# extensions.py

from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Only keep the relevant extensions
jwt = JWTManager()
cors = CORS()
