"""
Service de diagnostic des maladies par photo
Intégration avec PlantVillage ou modèle IA custom
"""

import requests
import json
import base64
from typing import Dict, Optional, List
from PIL import Image
import io
from datetime import datetime
from src.services.pineapple_service import PineappleService

class DiseaseDetectionService:
    """Service pour détecter les maladies des plantes par photo"""
    
    def __init__(self, api_key: str = None, model_url: str = None):
        self.api_key = api_key
        self.model_url = model_url or "https://api.plantvillage.org/detect"  # URL par défaut
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def detect_disease(self, image_data: bytes, culture: str = 'mais') -> Optional[Dict]:
        """
        Détecte les maladies des plantes à partir d'une image
        
        Args:
            image_data (bytes): Données de l'image
            culture (str): Culture concernée (mais, ananas)
            
        Returns:
            dict: Résultats du diagnostic ou None
        """
        try:
            # Prétraiter l'image
            processed_image = self._preprocess_image(image_data)
            
            if processed_image is None:
                return None
            
            # Appeler l'API de détection selon la culture
            if culture.lower() == 'ananas':
                return self._detect_pineapple_disease(processed_image)
            else:
                return self._detect_corn_disease(processed_image)
                
        except Exception as e:
            print(f"Erreur détection maladie: {e}")
            return None

    def _preprocess_image(self, image_data: bytes) -> Optional[bytes]:
        """
        Prétraite l'image pour l'analyse
        
        Args:
            image_data (bytes): Données brutes de l'image
            
        Returns:
            bytes: Image prétraitée ou None si erreur
        """
        try:
            # Ouvrir l'image avec PIL
            image = Image.open(io.BytesIO(image_data))
            
            # Redimensionner si nécessaire (max 1024x1024)
            max_size = (1024, 1024)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convertir en RGB si nécessaire
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Sauvegarder en bytes
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85)
            return output.getvalue()
            
        except Exception as e:
            print(f"Erreur lors du prétraitement: {e}")
            return None
    
    def _call_detection_api(self, image_data: bytes, culture: str) -> Optional[Dict]:
        """
        Appelle l'API de détection des maladies
        
        Args:
            image_data (bytes): Image prétraitée
            culture (str): Culture concernée
            
        Returns:
            dict: Résultats de l'API ou None si erreur
        """
        try:
            # Encoder l'image en base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Préparer les données pour l'API
            payload = {
                'image': image_base64,
                'culture': culture,
                'format': 'json'
            }
            
            # Appel à l'API
            response = self.session.post(
                self.model_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erreur API détection: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erreur lors de l'appel API: {e}")
            return None
    
    def _generate_diagnosis(self, detection_result: Dict, culture: str) -> Dict:
        """
        Génère un diagnostic complet basé sur les résultats de détection
        
        Args:
            detection_result (dict): Résultats de l'API
            culture (str): Culture concernée
            
        Returns:
            dict: Diagnostic complet
        """
        # Extraction des informations de base
        disease_name = detection_result.get('disease', 'Maladie non identifiée')
        confidence = detection_result.get('confidence', 0)
        symptoms = detection_result.get('symptoms', [])
        
        # Génération du diagnostic
        diagnosis = {
            'culture': culture,
            'disease_name': disease_name,
            'confidence': confidence,
            'symptoms': symptoms,
            'severity': self._assess_severity(confidence),
            'treatments': self._get_treatments(disease_name, culture),
            'prevention': self._get_prevention(disease_name, culture),
            'recommendations': self._get_recommendations(disease_name, culture)
        }
        
        return diagnosis
    
    def _assess_severity(self, confidence: float) -> str:
        """
        Évalue la sévérité basée sur la confiance
        
        Args:
            confidence (float): Niveau de confiance (0-1)
            
        Returns:
            str: Niveau de sévérité
        """
        if confidence > 0.8:
            return "Élevée"
        elif confidence > 0.6:
            return "Modérée"
        elif confidence > 0.4:
            return "Faible"
        else:
            return "Incertaine"
    
    def _get_treatments(self, disease_name: str, culture: str) -> List[Dict]:
        """
        Retourne les traitements pour une maladie donnée
        
        Args:
            disease_name (str): Nom de la maladie
            culture (str): Culture concernée
            
        Returns:
            list: Liste des traitements
        """
        # Base de données des traitements (à enrichir)
        treatments_db = {
            'mais': {
                'charançon du maïs': [
                    {
                        'name': 'Traitement chimique',
                        'description': 'Application d\'insecticides systémiques',
                        'products': ['Carbofuran', 'Imidacloprid'],
                        'application': 'Au moment du semis ou en traitement foliaire'
                    },
                    {
                        'name': 'Traitement biologique',
                        'description': 'Utilisation de nématodes entomopathogènes',
                        'products': ['Steinernema carpocapsae'],
                        'application': 'Application au sol avant semis'
                    }
                ],
                'pourriture des tiges': [
                    {
                        'name': 'Fongicide',
                        'description': 'Application de fongicides systémiques',
                        'products': ['Tebuconazole', 'Azoxystrobin'],
                        'application': 'Traitement préventif ou curatif'
                    },
                    {
                        'name': 'Rotation des cultures',
                        'description': 'Éviter la monoculture du maïs',
                        'products': ['Légumineuses', 'Céréales'],
                        'application': 'Planification de rotation sur 3-4 ans'
                    }
                ],
                'maladie des taches foliaires': [
                    {
                        'name': 'Fongicide foliaire',
                        'description': 'Application de fongicides de contact',
                        'products': ['Mancozèbe', 'Chlorothalonil'],
                        'application': 'Traitement dès l\'apparition des symptômes'
                    }
                ]
            }
        }
        
        return treatments_db.get(culture, {}).get(disease_name.lower(), [])
    
    def _get_prevention(self, disease_name: str, culture: str) -> List[str]:
        """
        Retourne les mesures de prévention
        
        Args:
            disease_name (str): Nom de la maladie
            culture (str): Culture concernée
            
        Returns:
            list: Liste des mesures de prévention
        """
        prevention_db = {
            'mais': {
                'charançon du maïs': [
                    'Semis précoce pour éviter les pics de population',
                    'Labour profond pour détruire les larves hivernantes',
                    'Rotation avec des cultures non-hôtes',
                    'Surveillance régulière des populations'
                ],
                'pourriture des tiges': [
                    'Éviter les sols compactés',
                    'Gestion équilibrée de l\'azote',
                    'Éviter les semis trop denses',
                    'Drainage approprié des sols'
                ],
                'maladie des taches foliaires': [
                    'Élimination des résidus de culture',
                    'Semis à densité appropriée',
                    'Fertilisation équilibrée',
                    'Variétés résistantes'
                ]
            }
        }
        
        return prevention_db.get(culture, {}).get(disease_name.lower(), [])
    
    def _get_recommendations(self, disease_name: str, culture: str) -> List[str]:
        """
        Retourne les recommandations générales
        
        Args:
            disease_name (str): Nom de la maladie
            culture (str): Culture concernée
            
        Returns:
            list: Liste des recommandations
        """
        recommendations = [
            'Consulter un expert agricole pour confirmation',
            'Documenter les symptômes observés',
            'Surveiller l\'évolution de la maladie',
            'Adapter les pratiques culturales',
            'Tenir un registre des traitements appliqués'
        ]
        
        return recommendations 

    def _detect_pineapple_disease(self, image_data: bytes) -> Optional[Dict]:
        """Détecte les maladies de l'ananas"""
        try:
            # Simuler l'appel à l'API PlantVillage pour ananas
            # En production, remplacer par l'appel réel à l'API
            
            # Données de test pour ananas
            pineapple_diseases = [
                {
                    'name': 'Fusariose',
                    'confidence': 0.85,
                    'severity': 'Élevée',
                    'symptoms': [
                        'Jaunissement des feuilles',
                        'Flétrissement progressif',
                        'Pourriture de la base de la tige',
                        'Décoloration rouge-brun des tissus'
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
                    ]
                },
                {
                    'name': 'Pourriture du cœur',
                    'confidence': 0.75,
                    'severity': 'Modérée',
                    'symptoms': [
                        'Pourriture du cœur',
                        'Feuilles centrales noircies',
                        'Odeur désagréable',
                        'Mort de la plante'
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
                    ]
                },
                {
                    'name': 'Cochenilles',
                    'confidence': 0.90,
                    'severity': 'Modérée',
                    'symptoms': [
                        'Présence de cochenilles blanches',
                        'Feuilles décolorées',
                        'Fruits déformés',
                        'Miellat sur les feuilles'
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
                    ]
                }
            ]
            
            # Simuler la détection (en production, utiliser l'API réelle)
            import random
            detected_disease = random.choice(pineapple_diseases)
            
            # Générer le diagnostic
            diagnosis = self._generate_pineapple_diagnosis(detected_disease, 'ananas')
            
            return diagnosis
            
        except Exception as e:
            print(f"Erreur détection maladie ananas: {e}")
            return None

    def _detect_corn_disease(self, image_data: bytes) -> Optional[Dict]:
        """Détecte les maladies du maïs (méthode existante)"""
        try:
            # Simuler l'appel à l'API PlantVillage pour maïs
            # En production, remplacer par l'appel réel à l'API
            
            # Données de test pour maïs (existantes)
            corn_diseases = [
                {
                    'name': 'charançon du maïs',
                    'confidence': 0.85,
                    'severity': 'Élevée',
                    'symptoms': [
                        'Trous caractéristiques dans les feuilles',
                        'Plants affaiblis et rabougris',
                        'Perte de rendement significative'
                    ],
                    'treatments': [
                        {
                            'name': 'Traitement chimique',
                            'description': 'Application d\'insecticides systémiques',
                            'products': ['Carbofuran', 'Imidacloprid'],
                            'application': 'Au moment du semis ou en traitement foliaire'
                        },
                        {
                            'name': 'Traitement biologique',
                            'description': 'Utilisation de nématodes entomopathogènes',
                            'products': ['Steinernema carpocapsae'],
                            'application': 'Application au sol avant semis'
                        }
                    ],
                    'prevention': [
                        'Semis précoce pour éviter les pics de population',
                        'Labour profond pour détruire les larves hivernantes',
                        'Rotation avec des cultures non-hôtes',
                        'Surveillance régulière des populations'
                    ]
                },
                {
                    'name': 'mildiou du maïs',
                    'confidence': 0.78,
                    'severity': 'Modérée',
                    'symptoms': [
                        'Taches grises sur les feuilles',
                        'Développement de moisissures',
                        'Affaiblissement des plants'
                    ],
                    'treatments': [
                        {
                            'name': 'Traitement fongicide',
                            'description': 'Application de fongicides',
                            'products': ['Mancozèbe', 'Chlorothalonil'],
                            'application': 'Pulvérisation préventive'
                        }
                    ],
                    'prevention': [
                        'Espacement approprié des plants',
                        'Éviter l\'irrigation par aspersion',
                        'Rotation des cultures',
                        'Destruction des débris infectés'
                    ]
                },
                {
                    'name': 'rouille du maïs',
                    'confidence': 0.82,
                    'severity': 'Modérée',
                    'symptoms': [
                        'Pustules rouges sur les feuilles',
                        'Affaiblissement des plants',
                        'Réduction du rendement'
                    ],
                    'treatments': [
                        {
                            'name': 'Traitement fongicide',
                            'description': 'Application de fongicides',
                            'products': ['Triadiméfon', 'Tébuconazole'],
                            'application': 'Pulvérisation curative'
                        }
                    ],
                    'prevention': [
                        'Utilisation de variétés résistantes',
                        'Rotation des cultures',
                        'Destruction des débris',
                        'Surveillance précoce'
                    ]
                }
            ]
            
            # Simuler la détection (en production, utiliser l'API réelle)
            import random
            detected_disease = random.choice(corn_diseases)
            
            # Générer le diagnostic
            diagnosis = self._generate_diagnosis(detected_disease, 'mais')
            
            return diagnosis
            
        except Exception as e:
            print(f"Erreur détection maladie maïs: {e}")
            return None

    def _generate_pineapple_diagnosis(self, disease_data: Dict, culture: str) -> Dict:
        """Génère un diagnostic détaillé pour ananas"""
        try:
            return {
                'culture': culture,
                'disease_name': disease_data['name'],
                'confidence': disease_data['confidence'],
                'severity': disease_data['severity'],
                'symptoms': disease_data['symptoms'],
                'treatments': disease_data['treatments'],
                'prevention': disease_data['prevention'],
                'diagnosis_date': datetime.now().isoformat(),
                'recommendations': [
                    'Consulter un expert agricole pour confirmation',
                    'Appliquer les traitements recommandés rapidement',
                    'Surveiller l\'évolution de la maladie',
                    'Adopter les mesures de prévention'
                ]
            }
            
        except Exception as e:
            print(f"Erreur génération diagnostic ananas: {e}")
            return {}

    def get_disease_info(self, disease_name: str, culture: str = 'mais') -> Optional[Dict]:
        """Récupère les informations sur une maladie spécifique"""
        try:
            if culture.lower() == 'ananas':
                # Récupérer depuis le service ananas
                return PineappleService().get_disease_by_name(disease_name)
            else:
                # Maladies du maïs (existantes)
                corn_diseases = {
                    'charançon du maïs': {
                        'name': 'charançon du maïs',
                        'scientific_name': 'Sitophilus zeamais',
                        'description': 'Insecte ravageur du maïs en stockage',
                        'symptoms': [
                            'Trous dans les grains',
                            'Poussière dans le stockage',
                            'Grains creux'
                        ],
                        'treatments': [
                            {
                                'name': 'Traitement préventif',
                                'description': 'Fumigation des stocks',
                                'products': ['Phosphine'],
                                'application': 'En stockage'
                            }
                        ],
                        'prevention': [
                            'Séchage correct des grains',
                            'Stockage hermétique',
                            'Surveillance régulière'
                        ]
                    }
                }
                return corn_diseases.get(disease_name.lower())
                
        except Exception as e:
            print(f"Erreur récupération info maladie: {e}")
            return None 