"""
Modèles pour la base de données ananas
Variétés, techniques culturales, données économiques
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class PineappleVariety(db.Model):
    """Modèle pour les variétés d'ananas"""
    
    __tablename__ = 'pineapple_varieties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    characteristics = db.Column(db.Text)  # JSON des caractéristiques
    yield_per_ha = db.Column(db.Float)  # Rendement en tonnes/ha
    cycle_duration = db.Column(db.Integer)  # Durée du cycle en mois
    resistance_diseases = db.Column(db.Text)  # JSON des résistances
    market_demand = db.Column(db.String(50))  # Élevée, Modérée, Faible
    price_per_kg = db.Column(db.Float)  # Prix moyen en FCFA
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_characteristics(self):
        """Récupère les caractéristiques parsées"""
        if self.characteristics:
            try:
                return json.loads(self.characteristics)
            except:
                return {}
        return {}
    
    def set_characteristics(self, characteristics_dict):
        """Définit les caractéristiques"""
        self.characteristics = json.dumps(characteristics_dict)
    
    def get_resistance_diseases(self):
        """Récupère les résistances parsées"""
        if self.resistance_diseases:
            try:
                return json.loads(self.resistance_diseases)
            except:
                return {}
        return {}
    
    def set_resistance_diseases(self, resistance_dict):
        """Définit les résistances"""
        self.resistance_diseases = json.dumps(resistance_dict)
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'description': self.description,
            'characteristics': self.get_characteristics(),
            'yield_per_ha': self.yield_per_ha,
            'cycle_duration': self.cycle_duration,
            'resistance_diseases': self.get_resistance_diseases(),
            'market_demand': self.market_demand,
            'price_per_kg': self.price_per_kg,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PineappleVariety {self.name}>'

class PineappleTechnique(db.Model):
    """Modèle pour les techniques culturales ananas"""
    
    __tablename__ = 'pineapple_techniques'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # plantation, entretien, récolte, post-récolte
    description = db.Column(db.Text)
    steps = db.Column(db.Text)  # JSON des étapes
    requirements = db.Column(db.Text)  # JSON des exigences
    duration_days = db.Column(db.Integer)  # Durée en jours
    cost_per_ha = db.Column(db.Float)  # Coût en FCFA/ha
    zone_agro_ecologique = db.Column(db.String(100))  # Zone applicable
    season = db.Column(db.String(50))  # Saison recommandée
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_steps(self):
        """Récupère les étapes parsées"""
        if self.steps:
            try:
                return json.loads(self.steps)
            except:
                return []
        return []
    
    def set_steps(self, steps_list):
        """Définit les étapes"""
        self.steps = json.dumps(steps_list)
    
    def get_requirements(self):
        """Récupère les exigences parsées"""
        if self.requirements:
            try:
                return json.loads(self.requirements)
            except:
                return {}
        return {}
    
    def set_requirements(self, requirements_dict):
        """Définit les exigences"""
        self.requirements = json.dumps(requirements_dict)
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'steps': self.get_steps(),
            'requirements': self.get_requirements(),
            'duration_days': self.duration_days,
            'cost_per_ha': self.cost_per_ha,
            'zone_agro_ecologique': self.zone_agro_ecologique,
            'season': self.season,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PineappleTechnique {self.name}>'

class PineappleDisease(db.Model):
    """Modèle pour les maladies de l'ananas"""
    
    __tablename__ = 'pineapple_diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)  # JSON des symptômes
    causes = db.Column(db.Text)  # JSON des causes
    treatments = db.Column(db.Text)  # JSON des traitements
    prevention = db.Column(db.Text)  # JSON des préventions
    severity = db.Column(db.String(50))  # Élevée, Modérée, Faible
    affected_parts = db.Column(db.Text)  # JSON des parties affectées
    season_risk = db.Column(db.String(50))  # Saison à risque
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_symptoms(self):
        """Récupère les symptômes parsés"""
        if self.symptoms:
            try:
                return json.loads(self.symptoms)
            except:
                return []
        return []
    
    def set_symptoms(self, symptoms_list):
        """Définit les symptômes"""
        self.symptoms = json.dumps(symptoms_list)
    
    def get_causes(self):
        """Récupère les causes parsées"""
        if self.causes:
            try:
                return json.loads(self.causes)
            except:
                return []
        return []
    
    def set_causes(self, causes_list):
        """Définit les causes"""
        self.causes = json.dumps(causes_list)
    
    def get_treatments(self):
        """Récupère les traitements parsés"""
        if self.treatments:
            try:
                return json.loads(self.treatments)
            except:
                return []
        return []
    
    def set_treatments(self, treatments_list):
        """Définit les traitements"""
        self.treatments = json.dumps(treatments_list)
    
    def get_prevention(self):
        """Récupère les préventions parsées"""
        if self.prevention:
            try:
                return json.loads(self.prevention)
            except:
                return []
        return []
    
    def set_prevention(self, prevention_list):
        """Définit les préventions"""
        self.prevention = json.dumps(prevention_list)
    
    def get_affected_parts(self):
        """Récupère les parties affectées parsées"""
        if self.affected_parts:
            try:
                return json.loads(self.affected_parts)
            except:
                return []
        return []
    
    def set_affected_parts(self, parts_list):
        """Définit les parties affectées"""
        self.affected_parts = json.dumps(parts_list)
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'description': self.description,
            'symptoms': self.get_symptoms(),
            'causes': self.get_causes(),
            'treatments': self.get_treatments(),
            'prevention': self.get_prevention(),
            'severity': self.severity,
            'affected_parts': self.get_affected_parts(),
            'season_risk': self.season_risk,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PineappleDisease {self.name}>'

class PineappleMarketData(db.Model):
    """Modèle pour les données de marché ananas"""
    
    __tablename__ = 'pineapple_market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    zone = db.Column(db.String(100), nullable=False)
    variety_id = db.Column(db.Integer, db.ForeignKey('pineapple_varieties.id'))
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    average_price = db.Column(db.Float)  # Prix moyen en FCFA/kg
    min_price = db.Column(db.Float)  # Prix minimum
    max_price = db.Column(db.Float)  # Prix maximum
    demand_level = db.Column(db.String(50))  # Élevée, Modérée, Faible
    supply_level = db.Column(db.String(50))  # Élevée, Modérée, Faible
    market_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    variety = db.relationship('PineappleVariety', backref='market_data')
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'zone': self.zone,
            'variety_id': self.variety_id,
            'variety_name': self.variety.name if self.variety else None,
            'month': self.month,
            'year': self.year,
            'average_price': self.average_price,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'demand_level': self.demand_level,
            'supply_level': self.supply_level,
            'market_notes': self.market_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PineappleMarketData {self.zone} - {self.month}/{self.year}>'

class PineappleEconomicData(db.Model):
    """Modèle pour les données économiques ananas"""
    
    __tablename__ = 'pineapple_economic_data'
    
    id = db.Column(db.Integer, primary_key=True)
    zone = db.Column(db.String(100), nullable=False)
    variety_id = db.Column(db.Integer, db.ForeignKey('pineapple_varieties.id'))
    surface_ha = db.Column(db.Float)  # Surface en hectares
    production_cost_per_ha = db.Column(db.Float)  # Coût de production FCFA/ha
    yield_per_ha = db.Column(db.Float)  # Rendement tonnes/ha
    revenue_per_ha = db.Column(db.Float)  # Revenu FCFA/ha
    profit_per_ha = db.Column(db.Float)  # Profit FCFA/ha
    roi_percentage = db.Column(db.Float)  # Retour sur investissement %
    break_even_price = db.Column(db.Float)  # Prix d'équilibre FCFA/kg
    season = db.Column(db.String(50))  # Saison de production
    year = db.Column(db.Integer)  # Année de référence
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    variety = db.relationship('PineappleVariety', backref='economic_data')
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'zone': self.zone,
            'variety_id': self.variety_id,
            'variety_name': self.variety.name if self.variety else None,
            'surface_ha': self.surface_ha,
            'production_cost_per_ha': self.production_cost_per_ha,
            'yield_per_ha': self.yield_per_ha,
            'revenue_per_ha': self.revenue_per_ha,
            'profit_per_ha': self.profit_per_ha,
            'roi_percentage': self.roi_percentage,
            'break_even_price': self.break_even_price,
            'season': self.season,
            'year': self.year,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PineappleEconomicData {self.zone} - {self.variety.name if self.variety else "Unknown"}>' 