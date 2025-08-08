"""
Modèle pour les logs de diagnostic de maladies
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class DiagnosisLog(db.Model):
    """Modèle pour enregistrer les diagnostics de maladies"""
    
    __tablename__ = 'diagnosis_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    disease_name = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float, default=0.0)  # Niveau de confiance (0-1)
    severity = db.Column(db.String(50))  # Élevée, Modérée, Faible, Incertaine
    culture = db.Column(db.String(50), default='mais')  # Culture concernée
    photo_data = db.Column(db.Text)  # Photo en base64
    diagnosis_data = db.Column(db.Text)  # Données complètes du diagnostic en JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='diagnosis_logs')
    
    def get_diagnosis_data(self):
        """Récupère les données de diagnostic parsées"""
        if self.diagnosis_data:
            try:
                return json.loads(self.diagnosis_data)
            except:
                return {}
        return {}
    
    def set_diagnosis_data(self, data):
        """Définit les données de diagnostic"""
        self.diagnosis_data = json.dumps(data)
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'disease_name': self.disease_name,
            'confidence': self.confidence,
            'severity': self.severity,
            'culture': self.culture,
            'diagnosis_data': self.get_diagnosis_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<DiagnosisLog {self.disease_name} - {self.confidence:.1%}>' 