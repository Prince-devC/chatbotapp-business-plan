# Script de création d'un administrateur par défaut
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from werkzeug.security import generate_password_hash
from src.models.database import db, AdminUser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_default_admin():
    """Créer un administrateur par défaut"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'database', 'app.db'))}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        
        # Vérifier si un admin existe déjà
        existing_admin = AdminUser.query.first()
        if existing_admin:
            print("Un administrateur existe déjà.")
            return
        
        # Créer l'admin par défaut
        admin = AdminUser(
            username='admin',
            email='admin@chatbot-business-plan.com',
            password_hash=generate_password_hash('admin123')
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("Administrateur par défaut créé:")
        print("Username: admin")
        print("Password: admin123")
        print("IMPORTANT: Changez ce mot de passe en production!")

if __name__ == '__main__':
    create_default_admin()

