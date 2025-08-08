"""
Service pour la gestion des données ananas
Conseils spécifiques, business plans et analyses économiques
"""

import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json

class PineappleService:
    """Service pour la gestion des données ananas"""
    
    def __init__(self):
        self.varieties = self._load_pineapple_varieties()
        self.techniques = self._load_pineapple_techniques()
        self.diseases = self._load_pineapple_diseases()
        self.market_data = self._load_market_data()
        self.economic_data = self._load_economic_data()
        
    def _load_pineapple_varieties(self) -> List[Dict]:
        """Charge les variétés d'ananas"""
        return [
            {
                'id': 1,
                'name': 'Smooth Cayenne',
                'scientific_name': 'Ananas comosus var. comosus',
                'description': 'Variété la plus cultivée au monde, fruit cylindrique, chair jaune, goût sucré-acide',
                'characteristics': {
                    'fruit_weight': '1.5-2.5 kg',
                    'fruit_shape': 'Cylindrique',
                    'flesh_color': 'Jaune',
                    'taste': 'Sucré-acide',
                    'shelf_life': '2-3 semaines',
                    'transport_resistance': 'Élevée'
                },
                'yield_per_ha': 35.0,  # tonnes/ha
                'cycle_duration': 18,  # mois
                'resistance_diseases': {
                    'fusariose': 'Modérée',
                    'pourriture_du_coeur': 'Faible',
                    'nématodes': 'Faible',
                    'cochenilles': 'Modérée'
                },
                'market_demand': 'Élevée',
                'price_per_kg': 250.0  # FCFA/kg
            },
            {
                'id': 2,
                'name': 'Queen Victoria',
                'scientific_name': 'Ananas comosus var. bracteatus',
                'description': 'Variété compacte, fruit petit mais très sucré, adaptée aux petits exploitants',
                'characteristics': {
                    'fruit_weight': '0.8-1.2 kg',
                    'fruit_shape': 'Conique',
                    'flesh_color': 'Jaune doré',
                    'taste': 'Très sucré',
                    'shelf_life': '3-4 semaines',
                    'transport_resistance': 'Modérée'
                },
                'yield_per_ha': 25.0,
                'cycle_duration': 15,
                'resistance_diseases': {
                    'fusariose': 'Élevée',
                    'pourriture_du_coeur': 'Modérée',
                    'nématodes': 'Modérée',
                    'cochenilles': 'Élevée'
                },
                'market_demand': 'Modérée',
                'price_per_kg': 300.0
            },
            {
                'id': 3,
                'name': 'MD2 (Golden)',
                'scientific_name': 'Ananas comosus var. comosus',
                'description': 'Variété premium, très sucrée, chair dorée, haute valeur commerciale',
                'characteristics': {
                    'fruit_weight': '1.8-2.2 kg',
                    'fruit_shape': 'Cylindrique',
                    'flesh_color': 'Doré',
                    'taste': 'Très sucré',
                    'shelf_life': '4-5 semaines',
                    'transport_resistance': 'Très élevée'
                },
                'yield_per_ha': 40.0,
                'cycle_duration': 20,
                'resistance_diseases': {
                    'fusariose': 'Élevée',
                    'pourriture_du_coeur': 'Modérée',
                    'nématodes': 'Modérée',
                    'cochenilles': 'Élevée'
                },
                'market_demand': 'Très élevée',
                'price_per_kg': 400.0
            }
        ]
    
    def _load_pineapple_techniques(self) -> List[Dict]:
        """Charge les techniques culturales ananas"""
        return [
            {
                'id': 1,
                'name': 'Préparation du sol',
                'category': 'plantation',
                'description': 'Préparation optimale du sol pour la plantation d\'ananas',
                'steps': [
                    'Labour profond (25-30 cm)',
                    'Nivellement du terrain',
                    'Préparation des billons (1.2-1.5 m de large)',
                    'Application de matière organique (10-15 t/ha)',
                    'Test de pH (optimal: 4.5-5.5)'
                ],
                'requirements': {
                    'soil_type': 'Sableux à limoneux',
                    'ph_range': '4.5-5.5',
                    'organic_matter': '10-15 t/ha',
                    'drainage': 'Bien drainé'
                },
                'duration_days': 7,
                'cost_per_ha': 150000,
                'zone_agro_ecologique': 'Toutes zones',
                'season': 'Début saison des pluies'
            },
            {
                'id': 2,
                'name': 'Plantation',
                'category': 'plantation',
                'description': 'Techniques de plantation des rejets d\'ananas',
                'steps': [
                    'Sélection de rejets sains (30-40 cm)',
                    'Traitement des rejets (désinfection)',
                    'Espacement: 30x60 cm (55 000 plants/ha)',
                    'Plantation en quinconce',
                    'Arrosage immédiat après plantation'
                ],
                'requirements': {
                    'planting_material': 'Rejets sains',
                    'density': '55 000 plants/ha',
                    'spacing': '30x60 cm',
                    'irrigation': 'Immédiate'
                },
                'duration_days': 14,
                'cost_per_ha': 200000,
                'zone_agro_ecologique': 'Toutes zones',
                'season': 'Début saison des pluies'
            },
            {
                'id': 3,
                'name': 'Fertilisation',
                'category': 'entretien',
                'description': 'Programme de fertilisation pour ananas',
                'steps': [
                    'Fertilisation de fond (NPK 15-15-15)',
                    'Apport azoté 3 mois après plantation',
                    'Fertilisation potassique 6 mois après plantation',
                    'Fertilisation foliaire (oligo-éléments)',
                    'Apport de magnésium si nécessaire'
                ],
                'requirements': {
                    'npk_ratio': '15-15-15',
                    'nitrogen_timing': '3 mois après plantation',
                    'potassium_timing': '6 mois après plantation',
                    'micronutrients': 'Fertilisation foliaire'
                },
                'duration_days': 365,
                'cost_per_ha': 180000,
                'zone_agro_ecologique': 'Toutes zones',
                'season': 'Toute l\'année'
            },
            {
                'id': 4,
                'name': 'Lutte contre les mauvaises herbes',
                'category': 'entretien',
                'description': 'Gestion des mauvaises herbes en culture ananas',
                'steps': [
                    'Désherbage manuel les 3 premiers mois',
                    'Application d\'herbicides sélectifs',
                    'Paillage avec matière organique',
                    'Entretien des allées',
                    'Surveillance continue'
                ],
                'requirements': {
                    'manual_weeding': '3 premiers mois',
                    'herbicides': 'Sélectifs',
                    'mulching': 'Matière organique',
                    'frequency': 'Mensuelle'
                },
                'duration_days': 365,
                'cost_per_ha': 120000,
                'zone_agro_ecologique': 'Toutes zones',
                'season': 'Toute l\'année'
            },
            {
                'id': 5,
                'name': 'Récolte',
                'category': 'récolte',
                'description': 'Techniques de récolte optimale des ananas',
                'steps': [
                    'Détermination de la maturité (œil ouvert)',
                    'Récolte tôt le matin',
                    'Coupe avec couteau bien aiguisé',
                    'Élimination des feuilles de couronne',
                    'Tri et calibrage'
                ],
                'requirements': {
                    'maturity_indicator': 'Œil ouvert',
                    'harvest_time': 'Tôt le matin',
                    'tools': 'Couteau aiguisé',
                    'grading': 'Tri par taille'
                },
                'duration_days': 30,
                'cost_per_ha': 80000,
                'zone_agro_ecologique': 'Toutes zones',
                'season': 'Saison de récolte'
            }
        ]
    
    def _load_pineapple_diseases(self) -> List[Dict]:
        """Charge les maladies de l'ananas"""
        return [
            {
                'id': 1,
                'name': 'Fusariose',
                'scientific_name': 'Fusarium oxysporum f. sp. ananassi',
                'description': 'Maladie fongique grave affectant les racines et la base de la tige',
                'symptoms': [
                    'Jaunissement des feuilles',
                    'Flétrissement progressif',
                    'Pourriture de la base de la tige',
                    'Décoloration rouge-brun des tissus'
                ],
                'causes': [
                    'Sol contaminé',
                    'Rejets infectés',
                    'Conditions humides',
                    'pH élevé'
                ],
                'treatments': [
                    {
                        'name': 'Traitement préventif',
                        'description': 'Désinfection des rejets avant plantation',
                        'products': ['Fongicides systémiques'],
                        'application': 'Trempage des rejets'
                    },
                    {
                        'name': 'Traitement curatif',
                        'description': 'Application de fongicides au sol',
                        'products': ['Carbendazime', 'Thiophanate-méthyl'],
                        'application': 'Arrosage au pied'
                    }
                ],
                'prevention': [
                    'Utilisation de rejets sains',
                    'Rotation des cultures',
                    'Drainage du sol',
                    'Contrôle du pH'
                ],
                'severity': 'Élevée',
                'affected_parts': ['Racines', 'Base de la tige', 'Feuilles'],
                'season_risk': 'Saison des pluies'
            },
            {
                'id': 2,
                'name': 'Pourriture du cœur',
                'scientific_name': 'Phytophthora parasitica',
                'description': 'Maladie fongique affectant le cœur de la plante',
                'symptoms': [
                    'Pourriture du cœur',
                    'Feuilles centrales noircies',
                    'Odeur désagréable',
                    'Mort de la plante'
                ],
                'causes': [
                    'Eau stagnante',
                    'Sol mal drainé',
                    'Plantation dense',
                    'Conditions humides'
                ],
                'treatments': [
                    {
                        'name': 'Traitement préventif',
                        'description': 'Amélioration du drainage',
                        'products': ['Amélioration du sol'],
                        'application': 'Travail du sol'
                    },
                    {
                        'name': 'Traitement curatif',
                        'description': 'Application de fongicides',
                        'products': ['Métalaxyl', 'Fosétyl-aluminium'],
                        'application': 'Pulvérisation'
                    }
                ],
                'prevention': [
                    'Drainage approprié',
                    'Espacement adéquat',
                    'Éviter l\'irrigation excessive',
                    'Rotation des cultures'
                ],
                'severity': 'Modérée',
                'affected_parts': ['Cœur de la plante', 'Feuilles centrales'],
                'season_risk': 'Saison des pluies'
            },
            {
                'id': 3,
                'name': 'Cochenilles',
                'scientific_name': 'Dysmicoccus brevipes',
                'description': 'Insectes suceurs affectant les feuilles et les fruits',
                'symptoms': [
                    'Présence de cochenilles blanches',
                    'Feuilles décolorées',
                    'Fruits déformés',
                    'Miellat sur les feuilles'
                ],
                'causes': [
                    'Plantation dense',
                    'Manque d\'aération',
                    'Conditions humides',
                    'Absence de lutte'
                ],
                'treatments': [
                    {
                        'name': 'Traitement biologique',
                        'description': 'Introduction d\'auxiliaires',
                        'products': ['Cryptolaemus montrouzieri'],
                        'application': 'Lâcher d\'auxiliaires'
                    },
                    {
                        'name': 'Traitement chimique',
                        'description': 'Application d\'insecticides',
                        'products': ['Imidacloprid', 'Acétamipride'],
                        'application': 'Pulvérisation'
                    }
                ],
                'prevention': [
                    'Espacement approprié',
                    'Aération des plantations',
                    'Surveillance régulière',
                    'Élimination des débris'
                ],
                'severity': 'Modérée',
                'affected_parts': ['Feuilles', 'Fruits', 'Tige'],
                'season_risk': 'Saison sèche'
            }
        ]
    
    def _load_market_data(self) -> List[Dict]:
        """Charge les données de marché ananas"""
        return [
            {
                'zone': 'Zone des terres de barre',
                'variety': 'Smooth Cayenne',
                'month': 1,
                'year': 2024,
                'average_price': 280,
                'min_price': 220,
                'max_price': 350,
                'demand_level': 'Élevée',
                'supply_level': 'Modérée',
                'market_notes': 'Période de forte demande, prix élevés'
            },
            {
                'zone': 'Zone des terres de barre',
                'variety': 'Smooth Cayenne',
                'month': 6,
                'year': 2024,
                'average_price': 200,
                'min_price': 150,
                'max_price': 250,
                'demand_level': 'Modérée',
                'supply_level': 'Élevée',
                'market_notes': 'Période de récolte, offre abondante'
            },
            {
                'zone': 'Zone des terres de barre',
                'variety': 'Queen Victoria',
                'month': 1,
                'year': 2024,
                'average_price': 320,
                'min_price': 280,
                'max_price': 380,
                'demand_level': 'Modérée',
                'supply_level': 'Faible',
                'market_notes': 'Variété premium, demande stable'
            }
        ]
    
    def _load_economic_data(self) -> List[Dict]:
        """Charge les données économiques ananas"""
        return [
            {
                'zone': 'Zone des terres de barre',
                'variety': 'Smooth Cayenne',
                'surface_ha': 1.0,
                'production_cost_per_ha': 850000,
                'yield_per_ha': 35.0,
                'revenue_per_ha': 875000,
                'profit_per_ha': 25000,
                'roi_percentage': 2.9,
                'break_even_price': 242.9,
                'season': 'Saison des pluies',
                'year': 2024
            },
            {
                'zone': 'Zone des terres de barre',
                'variety': 'Queen Victoria',
                'surface_ha': 1.0,
                'production_cost_per_ha': 750000,
                'yield_per_ha': 25.0,
                'revenue_per_ha': 750000,
                'profit_per_ha': 0,
                'roi_percentage': 0.0,
                'break_even_price': 300.0,
                'season': 'Saison des pluies',
                'year': 2024
            },
            {
                'zone': 'Zone des terres de barre',
                'variety': 'MD2 (Golden)',
                'surface_ha': 1.0,
                'production_cost_per_ha': 1200000,
                'yield_per_ha': 40.0,
                'revenue_per_ha': 1600000,
                'profit_per_ha': 400000,
                'roi_percentage': 33.3,
                'break_even_price': 300.0,
                'season': 'Saison des pluies',
                'year': 2024
            }
        ]
    
    def get_varieties(self, zone: str = None) -> List[Dict]:
        """Récupère les variétés d'ananas"""
        if zone:
            # Filtrer par zone si nécessaire
            return [v for v in self.varieties if v.get('zone_compatibility', 'Toutes zones') == zone or v.get('zone_compatibility', 'Toutes zones') == 'Toutes zones']
        return self.varieties
    
    def get_variety_by_id(self, variety_id: int) -> Optional[Dict]:
        """Récupère une variété par ID"""
        for variety in self.varieties:
            if variety['id'] == variety_id:
                return variety
        return None
    
    def get_techniques(self, category: str = None, zone: str = None) -> List[Dict]:
        """Récupère les techniques culturales"""
        techniques = self.techniques
        
        if category:
            techniques = [t for t in techniques if t['category'] == category]
        
        if zone:
            techniques = [t for t in techniques if t['zone_agro_ecologique'] == zone or t['zone_agro_ecologique'] == 'Toutes zones']
        
        return techniques
    
    def get_diseases(self, severity: str = None) -> List[Dict]:
        """Récupère les maladies"""
        diseases = self.diseases
        
        if severity:
            diseases = [d for d in diseases if d['severity'] == severity]
        
        return diseases
    
    def get_disease_by_name(self, disease_name: str) -> Optional[Dict]:
        """Récupère une maladie par nom"""
        for disease in self.diseases:
            if disease['name'].lower() == disease_name.lower():
                return disease
        return None
    
    def get_market_data(self, zone: str, variety: str = None, month: int = None) -> List[Dict]:
        """Récupère les données de marché"""
        market_data = [d for d in self.market_data if d['zone'] == zone]
        
        if variety:
            market_data = [d for d in market_data if d['variety'] == variety]
        
        if month:
            market_data = [d for d in market_data if d['month'] == month]
        
        return market_data
    
    def get_economic_data(self, zone: str, variety: str = None) -> List[Dict]:
        """Récupère les données économiques"""
        economic_data = [d for d in self.economic_data if d['zone'] == zone]
        
        if variety:
            economic_data = [d for d in economic_data if d['variety'] == variety]
        
        return economic_data
    
    def generate_pineapple_business_plan(self, user_data: Dict, variety_id: int = 1) -> Dict:
        """Génère un business plan ananas"""
        try:
            # Récupérer la variété
            variety = self.get_variety_by_id(variety_id)
            if not variety:
                variety = self.varieties[0]  # Smooth Cayenne par défaut
            
            # Récupérer les données économiques
            zone = user_data.get('zone_agro_ecologique', 'Zone des terres de barre')
            economic_data = self.get_economic_data(zone, variety['name'])
            
            if not economic_data:
                economic_data = [self.economic_data[0]]  # Données par défaut
            
            eco_data = economic_data[0]
            
            # Calculs économiques
            surface_ha = user_data.get('land_area', 1.0)
            production_cost = eco_data['production_cost_per_ha'] * surface_ha
            expected_yield = eco_data['yield_per_ha'] * surface_ha
            expected_revenue = eco_data['revenue_per_ha'] * surface_ha
            expected_profit = eco_data['profit_per_ha'] * surface_ha
            
            # Techniques culturales
            techniques = self.get_techniques(zone=zone)
            
            # Calendrier cultural
            calendar = self._generate_pineapple_calendar(variety, zone)
            
            return {
                'variety': variety,
                'economic_summary': {
                    'surface_ha': surface_ha,
                    'production_cost': production_cost,
                    'expected_yield': expected_yield,
                    'expected_revenue': expected_revenue,
                    'expected_profit': expected_profit,
                    'roi_percentage': eco_data['roi_percentage'],
                    'break_even_price': eco_data['break_even_price']
                },
                'techniques': techniques,
                'calendar': calendar,
                'market_analysis': self._generate_market_analysis(zone, variety['name']),
                'risk_analysis': self._generate_risk_analysis(variety, zone),
                'recommendations': self._generate_recommendations(variety, zone, user_data)
            }
            
        except Exception as e:
            print(f"Erreur génération business plan ananas: {e}")
            return {}
    
    def _generate_pineapple_calendar(self, variety: Dict, zone: str) -> Dict:
        """Génère un calendrier cultural ananas"""
        cycle_duration = variety.get('cycle_duration', 18)
        
        calendar = {
            'cycle_duration_months': cycle_duration,
            'phases': [
                {
                    'phase': 'Préparation du sol',
                    'duration': '1 mois',
                    'activities': [
                        'Labour profond',
                        'Préparation des billons',
                        'Application de matière organique'
                    ]
                },
                {
                    'phase': 'Plantation',
                    'duration': '1 mois',
                    'activities': [
                        'Sélection des rejets',
                        'Plantation en quinconce',
                        'Arrosage initial'
                    ]
                },
                {
                    'phase': 'Entretien (1-6 mois)',
                    'duration': '6 mois',
                    'activities': [
                        'Désherbage manuel',
                        'Fertilisation azotée',
                        'Lutte contre les mauvaises herbes'
                    ]
                },
                {
                    'phase': 'Entretien (7-12 mois)',
                    'duration': '6 mois',
                    'activities': [
                        'Fertilisation potassique',
                        'Lutte contre les ravageurs',
                        'Surveillance des maladies'
                    ]
                },
                {
                    'phase': 'Maturation (13-18 mois)',
                    'duration': '6 mois',
                    'activities': [
                        'Surveillance de la maturité',
                        'Préparation de la récolte',
                        'Organisation de la vente'
                    ]
                },
                {
                    'phase': 'Récolte',
                    'duration': '1 mois',
                    'activities': [
                        'Récolte sélective',
                        'Tri et calibrage',
                        'Commercialisation'
                    ]
                }
            ]
        }
        
        return calendar
    
    def _generate_market_analysis(self, zone: str, variety: str) -> Dict:
        """Génère une analyse de marché"""
        market_data = self.get_market_data(zone, variety)
        
        if not market_data:
            return {
                'average_price': 250,
                'price_range': '200-300 FCFA/kg',
                'demand_level': 'Modérée',
                'supply_level': 'Modérée',
                'market_trend': 'Stable',
                'recommendations': [
                    'Surveiller les prix de marché',
                    'Diversifier les canaux de vente',
                    'Établir des contrats de vente'
                ]
            }
        
        # Calculer les moyennes
        avg_price = sum(d['average_price'] for d in market_data) / len(market_data)
        min_price = min(d['min_price'] for d in market_data)
        max_price = max(d['max_price'] for d in market_data)
        
        return {
            'average_price': avg_price,
            'price_range': f'{min_price}-{max_price} FCFA/kg',
            'demand_level': market_data[0]['demand_level'],
            'supply_level': market_data[0]['supply_level'],
            'market_trend': 'Stable',
            'recommendations': [
                'Surveiller les prix de marché',
                'Diversifier les canaux de vente',
                'Établir des contrats de vente',
                'Optimiser la qualité pour obtenir de meilleurs prix'
            ]
        }
    
    def _generate_risk_analysis(self, variety: Dict, zone: str) -> Dict:
        """Génère une analyse des risques"""
        diseases = self.get_diseases()
        
        return {
            'climatic_risks': [
                'Sécheresse prolongée',
                'Pluies excessives',
                'Températures extrêmes'
            ],
            'disease_risks': [
                disease['name'] for disease in diseases if disease['severity'] in ['Élevée', 'Modérée']
            ],
            'market_risks': [
                'Fluctuation des prix',
                'Concurrence accrue',
                'Changement des préférences'
            ],
            'mitigation_strategies': [
                'Irrigation de secours',
                'Drainage approprié',
                'Lutte préventive contre les maladies',
                'Diversification des variétés',
                'Contrats de vente'
            ]
        }
    
    def _generate_recommendations(self, variety: Dict, zone: str, user_data: Dict) -> List[str]:
        """Génère des recommandations personnalisées"""
        recommendations = [
            f"Choisir la variété {variety['name']} pour sa {variety['market_demand']} demande",
            f"Planifier un cycle de {variety['cycle_duration']} mois",
            "Investir dans l'irrigation pour sécuriser la production",
            "Mettre en place un programme de fertilisation équilibré",
            "Surveiller régulièrement les maladies et ravageurs",
            "Établir des partenariats commerciaux avant la récolte"
        ]
        
        # Recommandations selon l'expérience
        experience = user_data.get('farming_experience', 'Débutant')
        if experience == 'Débutant':
            recommendations.extend([
                "Commencer avec une petite surface (0.5-1 ha)",
                "Se former aux techniques culturales",
                "S'associer avec des producteurs expérimentés"
            ])
        elif experience == 'Intermédiaire':
            recommendations.extend([
                "Optimiser les techniques culturales",
                "Investir dans la mécanisation",
                "Diversifier les variétés"
            ])
        else:  # Expérimenté
            recommendations.extend([
                "Augmenter la surface de production",
                "Investir dans la transformation",
                "Exporter vers les marchés internationaux"
            ])
        
        return recommendations
    
    def get_pineapple_advice(self, zone: str, variety: str = None, season: str = None) -> Dict:
        """Génère des conseils spécifiques ananas"""
        try:
            # Conseils généraux
            general_advice = [
                "L'ananas nécessite un sol bien drainé",
                "Le pH optimal est entre 4.5 et 5.5",
                "La plantation se fait en début de saison des pluies",
                "L'espacement recommandé est de 30x60 cm",
                "La fertilisation doit être équilibrée (NPK)"
            ]
            
            # Conseils par saison
            seasonal_advice = {
                'saison_des_pluies': [
                    "Préparer le sol avant les premières pluies",
                    "Planter dès le début de la saison",
                    "Surveiller le drainage",
                    "Lutter contre les mauvaises herbes"
                ],
                'saison_seche': [
                    "Irriguer régulièrement",
                    "Pailler pour conserver l'humidité",
                    "Surveiller les ravageurs",
                    "Préparer la récolte"
                ]
            }
            
            # Conseils par variété
            variety_advice = {}
            for var in self.varieties:
                variety_advice[var['name']] = [
                    f"Rendement attendu: {var['yield_per_ha']} t/ha",
                    f"Cycle de production: {var['cycle_duration']} mois",
                    f"Prix moyen: {var['price_per_kg']} FCFA/kg",
                    f"Demande: {var['market_demand']}"
                ]
            
            return {
                'general_advice': general_advice,
                'seasonal_advice': seasonal_advice.get(season, []),
                'variety_advice': variety_advice.get(variety, []),
                'zone_specific': f"Zone {zone}: conditions favorables pour l'ananas"
            }
            
        except Exception as e:
            print(f"Erreur génération conseils ananas: {e}")
            return {} 