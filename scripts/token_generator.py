import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
import datetime

# Créer une mini-application Flask pour générer le token
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
jwt = JWTManager(app)

with app.app_context():
    # Créer un token pour l'admin avec ID=1
    expires = datetime.timedelta(days=30)
    access_token = create_access_token(identity=1, expires_delta=expires)
    
    print("\n=== TOKEN JWT ADMIN ===")
    print(access_token)
    print("\n=== À COPIER DANS LE FRONTEND ===")
    print(f"ADMIN_JWT_TOKEN: '{access_token}'")
    print("===========================\n")
