"""
Service météo pour AgroBizChat
Intégration avec MeteoBenin.bj
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import os

class WeatherService:
    """Service pour récupérer les données météorologiques"""
    
    # Configuration API
    BASE_URL = "https://api.meteobenin.bj"
    SANDBOX_URL = "https://api-sandbox.meteobenin.bj"
    
    def __init__(self, api_key: str = None, use_sandbox: bool = True):
        self.api_key = api_key or os.getenv('METEOBENIN_API_KEY')
        self.use_sandbox = use_sandbox
        self.base_url = self.SANDBOX_URL if use_sandbox else self.BASE_URL
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
        
        # Mode développement avec données de test
        self.dev_mode = not self.api_key
    
    def get_current_weather(self, zone_agro_ecologique: str) -> Optional[Dict]:
        """
        Récupère la météo actuelle pour une zone agro-écologique
        
        Args:
            zone_agro_ecologique (str): Zone agro-écologique
            
        Returns:
            dict: Données météo ou None si erreur
        """
        try:
            if self.dev_mode:
                return self._get_mock_weather(zone_agro_ecologique)
            
            # Mapping des zones vers les coordonnées
            zone_coordinates = self._get_zone_coordinates(zone_agro_ecologique)
            if not zone_coordinates:
                return None
                
            response = self.session.get(
                f"{self.base_url}/api/v1/weather/current",
                params={
                    'lat': zone_coordinates['lat'],
                    'lon': zone_coordinates['lon']
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return self._parse_weather_data(response.json())
            else:
                print(f"Erreur API météo: {response.status_code}")
                return self._get_mock_weather(zone_agro_ecologique)
                
        except Exception as e:
            print(f"Erreur lors de la récupération météo: {e}")
            return self._get_mock_weather(zone_agro_ecologique)
    
    def get_forecast(self, zone_agro_ecologique: str, days: int = 7) -> Optional[List[Dict]]:
        """
        Récupère les prévisions météo
        
        Args:
            zone_agro_ecologique (str): Zone agro-écologique
            days (int): Nombre de jours de prévision
            
        Returns:
            list: Liste des prévisions ou None si erreur
        """
        try:
            if self.dev_mode:
                return self._get_mock_forecast(zone_agro_ecologique, days)
            
            zone_coordinates = self._get_zone_coordinates(zone_agro_ecologique)
            if not zone_coordinates:
                return None
                
            response = self.session.get(
                f"{self.base_url}/api/v1/weather/forecast",
                params={
                    'lat': zone_coordinates['lat'],
                    'lon': zone_coordinates['lon'],
                    'days': days
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return self._parse_forecast_data(response.json())
            else:
                print(f"Erreur API prévisions: {response.status_code}")
                return self._get_mock_forecast(zone_agro_ecologique, days)
                
        except Exception as e:
            print(f"Erreur lors de la récupération des prévisions: {e}")
            return self._get_mock_forecast(zone_agro_ecologique, days)
    
    def get_agro_advice(self, zone_agro_ecologique: str, culture: str) -> Optional[Dict]:
        """
        Génère des conseils agro-météo
        
        Args:
            zone_agro_ecologique (str): Zone agro-écologique
            culture (str): Culture concernée
            
        Returns:
            dict: Conseils agro-météo ou None si erreur
        """
        try:
            current_weather = self.get_current_weather(zone_agro_ecologique)
            if not current_weather:
                return None
                
            return self._generate_agro_advice(current_weather, culture)
            
        except Exception as e:
            print(f"Erreur lors de la génération des conseils: {e}")
            return None
    
    def _get_zone_coordinates(self, zone_agro_ecologique: str) -> Optional[Dict]:
        """
        Retourne les coordonnées pour une zone agro-écologique
        
        Args:
            zone_agro_ecologique (str): Zone agro-écologique
            
        Returns:
            dict: {'lat': float, 'lon': float} ou None
        """
        # Mapping des zones agro-écologiques du Bénin
        zone_mapping = {
            'Zone côtière': {'lat': 6.3690, 'lon': 2.4225, 'name': 'Cotonou'},
            'Zone des terres de barre': {'lat': 6.4969, 'lon': 2.6043, 'name': 'Abomey-Calavi'},
            'Zone des collines': {'lat': 7.1761, 'lon': 1.9911, 'name': 'Abomey'},
            'Zone de l\'Atacora': {'lat': 10.3049, 'lon': 1.3750, 'name': 'Natitingou'},
            'Zone de la Donga': {'lat': 9.7000, 'lon': 1.6667, 'name': 'Djougou'},
            'Zone de l\'Ouémé': {'lat': 6.6333, 'lon': 2.4667, 'name': 'Porto-Novo'},
            'Zone de l\'Alibori': {'lat': 11.3000, 'lon': 2.3500, 'name': 'Kandi'},
            'Zone du Borgou': {'lat': 9.7000, 'lon': 2.6000, 'name': 'Parakou'},
            'Zone du Mono': {'lat': 6.5000, 'lon': 1.7500, 'name': 'Lokossa'},
            'Zone du Couffo': {'lat': 6.8500, 'lon': 1.9500, 'name': 'Aplahoué'}
        }
        
        return zone_mapping.get(zone_agro_ecologique)
    
    def _get_mock_weather(self, zone_agro_ecologique: str) -> Dict:
        """
        Génère des données météo de test
        
        Args:
            zone_agro_ecologique (str): Zone agro-écologique
            
        Returns:
            dict: Données météo de test
        """
        import random
        
        # Données météo réalistes selon la zone
        zone_data = {
            'Zone côtière': {'temp_range': (25, 32), 'humidity_range': (70, 90)},
            'Zone des terres de barre': {'temp_range': (24, 30), 'humidity_range': (65, 85)},
            'Zone des collines': {'temp_range': (22, 28), 'humidity_range': (60, 80)},
            'Zone de l\'Atacora': {'temp_range': (20, 26), 'humidity_range': (55, 75)},
            'Zone de la Donga': {'temp_range': (21, 27), 'humidity_range': (60, 80)},
            'Zone de l\'Ouémé': {'temp_range': (25, 31), 'humidity_range': (70, 85)},
            'Zone de l\'Alibori': {'temp_range': (23, 29), 'humidity_range': (50, 70)},
            'Zone du Borgou': {'temp_range': (22, 28), 'humidity_range': (55, 75)},
            'Zone du Mono': {'temp_range': (24, 30), 'humidity_range': (65, 85)},
            'Zone du Couffo': {'temp_range': (23, 29), 'humidity_range': (60, 80)}
        }
        
        zone_config = zone_data.get(zone_agro_ecologique, {'temp_range': (24, 30), 'humidity_range': (60, 80)})
        
        temperature = random.uniform(*zone_config['temp_range'])
        humidity = random.uniform(*zone_config['humidity_range'])
        precipitation = random.uniform(0, 15)
        wind_speed = random.uniform(5, 15)
        
        descriptions = [
            "Ensoleillé avec quelques nuages",
            "Nuageux avec éclaircies",
            "Pluie légère",
            "Ciel dégagé",
            "Nuages épars"
        ]
        
        return {
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1),
            'precipitation': round(precipitation, 1),
            'wind_speed': round(wind_speed, 1),
            'description': random.choice(descriptions),
            'icon': 'sunny',
            'timestamp': datetime.now().isoformat(),
            'zone': zone_agro_ecologique
        }
    
    def _get_mock_forecast(self, zone_agro_ecologique: str, days: int) -> List[Dict]:
        """
        Génère des prévisions météo de test
        
        Args:
            zone_agro_ecologique (str): Zone agro-écologique
            days (int): Nombre de jours
            
        Returns:
            list: Prévisions de test
        """
        import random
        
        forecasts = []
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            
            # Variation réaliste des températures
            base_temp = random.uniform(24, 30)
            temp_max = base_temp + random.uniform(2, 5)
            temp_min = base_temp - random.uniform(2, 5)
            
            forecasts.append({
                'date': date.strftime('%Y-%m-%d'),
                'temperature_max': round(temp_max, 1),
                'temperature_min': round(temp_min, 1),
                'precipitation': round(random.uniform(0, 20), 1),
                'description': random.choice(['Ensoleillé', 'Nuageux', 'Pluie légère', 'Ciel dégagé']),
                'icon': 'sunny'
            })
        
        return forecasts
    
    def _parse_weather_data(self, data: Dict) -> Dict:
        """
        Parse les données météo brutes
        
        Args:
            data (dict): Données brutes de l'API
            
        Returns:
            dict: Données formatées
        """
        return {
            'temperature': data.get('temp', 0),
            'humidity': data.get('humidity', 0),
            'precipitation': data.get('precip', 0),
            'wind_speed': data.get('wind_speed', 0),
            'description': data.get('description', ''),
            'icon': data.get('icon', ''),
            'timestamp': datetime.now().isoformat(),
            'zone': data.get('zone', '')
        }
    
    def _parse_forecast_data(self, data: Dict) -> List[Dict]:
        """
        Parse les données de prévision
        
        Args:
            data (dict): Données brutes de l'API
            
        Returns:
            list: Liste des prévisions formatées
        """
        forecasts = []
        for day_data in data.get('daily', []):
            forecasts.append({
                'date': day_data.get('date', ''),
                'temperature_max': day_data.get('temp_max', 0),
                'temperature_min': day_data.get('temp_min', 0),
                'precipitation': day_data.get('precip', 0),
                'description': day_data.get('description', ''),
                'icon': day_data.get('icon', '')
            })
        return forecasts
    
    def _generate_agro_advice(self, weather: Dict, culture: str) -> Dict:
        """
        Génère des conseils agro-météo basés sur les conditions actuelles
        
        Args:
            weather (dict): Données météo actuelles
            culture (str): Culture concernée
            
        Returns:
            dict: Conseils agro-météo
        """
        temp = weather.get('temperature', 0)
        humidity = weather.get('humidity', 0)
        precip = weather.get('precipitation', 0)
        
        advice = {
            'culture': culture,
            'conditions_actuelles': {
                'temperature': f"{temp}°C",
                'humidity': f"{humidity}%",
                'precipitation': f"{precip}mm",
                'description': weather.get('description', ''),
                'zone': weather.get('zone', '')
            },
            'conseils': [],
            'risques': [],
            'recommandations': [],
            'actions_immediates': [],
            'planification': []
        }
        
        # Conseils spécifiques au maïs
        if culture.lower() == 'mais':
            if temp < 15:
                advice['conseils'].append("Température trop basse pour la croissance du maïs")
                advice['recommandations'].append("Attendre une hausse des températures avant les semis")
                advice['actions_immediates'].append("Reporter les semis de 1-2 semaines")
            elif temp > 35:
                advice['conseils'].append("Température élevée - risque de stress hydrique")
                advice['recommandations'].append("Arrosage supplémentaire recommandé")
                advice['actions_immediates'].append("Irriguer en soirée ou tôt le matin")
            
            if humidity < 40:
                advice['conseils'].append("Humidité faible")
                advice['recommandations'].append("Irrigation recommandée")
                advice['actions_immediates'].append("Programmer une irrigation")
            elif humidity > 80:
                advice['conseils'].append("Humidité élevée - risque de maladies fongiques")
                advice['recommandations'].append("Surveiller les signes de maladies")
                advice['actions_immediates'].append("Inspecter les plants pour détecter les maladies")
            
            if precip < 5:
                advice['conseils'].append("Faibles précipitations")
                advice['recommandations'].append("Irrigation nécessaire")
                advice['planification'].append("Prévoir un système d'irrigation")
            elif precip > 50:
                advice['conseils'].append("Fortes précipitations")
                advice['recommandations'].append("Éviter les travaux au champ")
                advice['actions_immediates'].append("Attendre que le sol soit moins humide")
            
            # Conseils généraux selon la saison
            current_month = datetime.now().month
            if current_month in [3, 4, 5]:  # Mars-Mai
                advice['planification'].append("Période idéale pour les semis de maïs")
            elif current_month in [6, 7, 8]:  # Juin-Août
                advice['planification'].append("Période de croissance - surveiller les besoins en eau")
            elif current_month in [9, 10, 11]:  # Septembre-Novembre
                advice['planification'].append("Période de maturation - préparer la récolte")
        
        return advice 