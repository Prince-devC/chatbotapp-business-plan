import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash
import datetime

# Importer les modèles
from src.models.database import db, AdminUser

# Créer une mini-application Flask
app = Flask(__name__)

# Configuration de la base de données
project_root = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(project_root, 'database', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
jwt = JWTManager(app)

# Initialiser la base de données
db.init_app(app)

def create_admin():
    with app.app_context():
        # Vérifier si l'admin existe déjà
        admin = AdminUser.query.filter_by(username='admin').first()
        
        if admin:
            print(f"L'administrateur 'admin' existe déjà (ID: {admin.id})")
        else:
            # Créer un nouvel administrateur
            admin = AdminUser(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Administrateur créé avec succès (ID: {admin.id})")
        
        # Générer un token JWT pour cet admin
        expires = datetime.timedelta(days=30)
        access_token = create_access_token(identity=admin.id, expires_delta=expires)
        
        print("\n=== TOKEN JWT ADMIN ===")
        print(access_token)
        print("\n=== À COPIER DANS LE FRONTEND ===")
        print(f"ADMIN_JWT_TOKEN: '{access_token}'")
        print("===========================\n")
        
        return admin, access_token

if __name__ == "__main__":
    admin, token = create_admin()
