"""
Modèles pour les paiements et abonnements
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class PaymentTransaction(db.Model):
    """Modèle pour les transactions de paiement"""
    
    __tablename__ = 'payment_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    package_id = db.Column(db.String(50), nullable=False)  # basic, premium, cooperative
    amount = db.Column(db.Integer, nullable=False)  # Montant en FCFA
    currency = db.Column(db.String(10), default='XOF')
    provider = db.Column(db.String(50), nullable=False)  # kkiapay, paydunya
    payment_id = db.Column(db.String(100), nullable=False)  # ID du paiement chez le provider
    reference = db.Column(db.String(100), nullable=False)  # Référence unique
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    payment_url = db.Column(db.String(500))  # URL de paiement
    paid_at = db.Column(db.DateTime)  # Date de paiement
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='payment_transactions')
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'package_id': self.package_id,
            'amount': self.amount,
            'currency': self.currency,
            'provider': self.provider,
            'payment_id': self.payment_id,
            'reference': self.reference,
            'status': self.status,
            'payment_url': self.payment_url,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PaymentTransaction {self.reference} - {self.status}>'

class Subscription(db.Model):
    """Modèle pour les abonnements utilisateur"""
    
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    package_id = db.Column(db.String(50), nullable=False)  # free, basic, premium, cooperative
    status = db.Column(db.String(20), default='active')  # active, cancelled, expired
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='subscriptions')
    
    @property
    def is_active(self):
        """Vérifie si l'abonnement est actif"""
        now = datetime.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date
        )
    
    @property
    def days_remaining(self):
        """Retourne le nombre de jours restants"""
        if not self.is_active:
            return 0
        
        remaining = self.end_date - datetime.now()
        return max(0, remaining.days)
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'package_id': self.package_id,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'days_remaining': self.days_remaining,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Subscription {self.package_id} - {self.status}>'

class Package(db.Model):
    """Modèle pour les packages de prix"""
    
    __tablename__ = 'packages'
    
    id = db.Column(db.String(50), primary_key=True)  # free, basic, premium, cooperative
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Prix en FCFA
    currency = db.Column(db.String(10), default='XOF')
    duration_days = db.Column(db.Integer, default=30)
    features = db.Column(db.Text)  # JSON des fonctionnalités
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_features(self):
        """Récupère les fonctionnalités parsées"""
        if self.features:
            try:
                return json.loads(self.features)
            except:
                return {}
        return {}
    
    def set_features(self, features_dict):
        """Définit les fonctionnalités"""
        self.features = json.dumps(features_dict)
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'currency': self.currency,
            'duration_days': self.duration_days,
            'features': self.get_features(),
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Package {self.name} - {self.price} {self.currency}>' 