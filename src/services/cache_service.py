"""
Service de cache Redis pour AgroBizChat
Optimisation des performances avec cache intelligent
"""

import redis
import json
import pickle
import hashlib
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import os

class CacheService:
    """Service de cache Redis pour optimiser les performances"""
    
    def __init__(self, redis_url: str = None):
        """
        Initialise le service de cache
        
        Args:
            redis_url (str): URL Redis (optionnel, utilise REDIS_URL par défaut)
        """
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis_client = None
        self.cache_enabled = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
        
        try:
            self.redis_client = redis.from_url(self.redis_url)
            # Test de connexion
            self.redis_client.ping()
            print(f"✅ Cache Redis connecté: {self.redis_url}")
        except Exception as e:
            print(f"⚠️ Cache Redis non disponible: {e}")
            self.cache_enabled = False
            self.redis_client = None
    
    def is_available(self) -> bool:
        """Vérifie si le cache est disponible"""
        if not self.cache_enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Génère une clé de cache unique
        
        Args:
            prefix (str): Préfixe de la clé
            *args: Arguments pour la clé
            **kwargs: Arguments nommés pour la clé
            
        Returns:
            str: Clé de cache unique
        """
        # Créer une chaîne unique
        key_parts = [prefix]
        
        # Ajouter les arguments positionnels
        for arg in args:
            key_parts.append(str(arg))
        
        # Ajouter les arguments nommés (triés pour la cohérence)
        for key, value in sorted(kwargs.items()):
            key_parts.append(f"{key}:{value}")
        
        # Créer un hash de la clé
        key_string = ":".join(key_parts)
        return f"agrobiz:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur du cache
        
        Args:
            key (str): Clé de cache
            default (any): Valeur par défaut si non trouvée
            
        Returns:
            any: Valeur en cache ou default
        """
        if not self.is_available():
            return default
        
        try:
            value = self.redis_client.get(key)
            if value is not None:
                return pickle.loads(value)
            return default
        except Exception as e:
            print(f"Erreur récupération cache: {e}")
            return default
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Stocke une valeur dans le cache
        
        Args:
            key (str): Clé de cache
            value (any): Valeur à stocker
            ttl (int): Time to live en secondes (défaut: 1h)
            
        Returns:
            bool: True si succès, False sinon
        """
        if not self.is_available():
            return False
        
        try:
            serialized_value = pickle.dumps(value)
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            print(f"Erreur stockage cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Supprime une clé du cache
        
        Args:
            key (str): Clé à supprimer
            
        Returns:
            bool: True si succès, False sinon
        """
        if not self.is_available():
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Erreur suppression cache: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Supprime toutes les clés correspondant à un pattern
        
        Args:
            pattern (str): Pattern Redis (ex: "agrobiz:weather:*")
            
        Returns:
            int: Nombre de clés supprimées
        """
        if not self.is_available():
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Erreur suppression pattern cache: {e}")
            return 0
    
    def get_or_set(self, key: str, callback: callable, ttl: int = 3600) -> Any:
        """
        Récupère une valeur du cache ou l'exécute et la stocke
        
        Args:
            key (str): Clé de cache
            callback (callable): Fonction à exécuter si pas en cache
            ttl (int): Time to live en secondes
            
        Returns:
            any: Valeur en cache ou résultat de callback
        """
        # Essayer de récupérer du cache
        cached_value = self.get(key)
        if cached_value is not None:
            return cached_value
        
        # Exécuter la fonction et stocker le résultat
        try:
            result = callback()
            self.set(key, result, ttl)
            return result
        except Exception as e:
            print(f"Erreur callback cache: {e}")
            return None
    
    def cache_weather_data(self, zone: str, weather_data: Dict) -> bool:
        """
        Cache les données météo
        
        Args:
            zone (str): Zone agro-écologique
            weather_data (dict): Données météo
            
        Returns:
            bool: True si succès
        """
        key = self._generate_key("weather", zone)
        return self.set(key, weather_data, ttl=1800)  # 30 minutes
    
    def get_cached_weather_data(self, zone: str) -> Optional[Dict]:
        """
        Récupère les données météo en cache
        
        Args:
            zone (str): Zone agro-écologique
            
        Returns:
            dict: Données météo ou None
        """
        key = self._generate_key("weather", zone)
        return self.get(key)
    
    def cache_pineapple_varieties(self, varieties: List[Dict]) -> bool:
        """
        Cache les variétés d'ananas
        
        Args:
            varieties (list): Liste des variétés
            
        Returns:
            bool: True si succès
        """
        key = self._generate_key("pineapple", "varieties")
        return self.set(key, varieties, ttl=7200)  # 2 heures
    
    def get_cached_pineapple_varieties(self) -> Optional[List[Dict]]:
        """
        Récupère les variétés d'ananas en cache
        
        Returns:
            list: Liste des variétés ou None
        """
        key = self._generate_key("pineapple", "varieties")
        return self.get(key)
    
    def cache_business_plan(self, user_id: int, plan_data: Dict) -> bool:
        """
        Cache un business plan
        
        Args:
            user_id (int): ID de l'utilisateur
            plan_data (dict): Données du business plan
            
        Returns:
            bool: True si succès
        """
        key = self._generate_key("business_plan", user_id)
        return self.set(key, plan_data, ttl=3600)  # 1 heure
    
    def get_cached_business_plan(self, user_id: int) -> Optional[Dict]:
        """
        Récupère un business plan en cache
        
        Args:
            user_id (int): ID de l'utilisateur
            
        Returns:
            dict: Business plan ou None
        """
        key = self._generate_key("business_plan", user_id)
        return self.get(key)
    
    def cache_disease_diagnosis(self, image_hash: str, diagnosis: Dict) -> bool:
        """
        Cache un diagnostic de maladie
        
        Args:
            image_hash (str): Hash de l'image
            diagnosis (dict): Résultats du diagnostic
            
        Returns:
            bool: True si succès
        """
        key = self._generate_key("diagnosis", image_hash)
        return self.set(key, diagnosis, ttl=86400)  # 24 heures
    
    def get_cached_diagnosis(self, image_hash: str) -> Optional[Dict]:
        """
        Récupère un diagnostic en cache
        
        Args:
            image_hash (str): Hash de l'image
            
        Returns:
            dict: Diagnostic ou None
        """
        key = self._generate_key("diagnosis", image_hash)
        return self.get(key)
    
    def cache_user_context(self, user_id: str, context: Dict) -> bool:
        """
        Cache le contexte utilisateur
        
        Args:
            user_id (str): ID de l'utilisateur
            context (dict): Contexte utilisateur
            
        Returns:
            bool: True si succès
        """
        key = self._generate_key("user_context", user_id)
        return self.set(key, context, ttl=1800)  # 30 minutes
    
    def get_cached_user_context(self, user_id: str) -> Optional[Dict]:
        """
        Récupère le contexte utilisateur en cache
        
        Args:
            user_id (str): ID de l'utilisateur
            
        Returns:
            dict: Contexte ou None
        """
        key = self._generate_key("user_context", user_id)
        return self.get(key)
    
    def clear_user_cache(self, user_id: str) -> bool:
        """
        Efface le cache d'un utilisateur
        
        Args:
            user_id (str): ID de l'utilisateur
            
        Returns:
            bool: True si succès
        """
        if not self.is_available():
            return False
        
        try:
            # Supprimer toutes les clés liées à l'utilisateur
            patterns = [
                f"agrobiz:business_plan:*{user_id}*",
                f"agrobiz:user_context:*{user_id}*",
                f"agrobiz:diagnosis:*{user_id}*"
            ]
            
            deleted_count = 0
            for pattern in patterns:
                deleted_count += self.clear_pattern(pattern)
            
            return deleted_count > 0
        except Exception as e:
            print(f"Erreur effacement cache utilisateur: {e}")
            return False
    
    def get_cache_stats(self) -> Dict:
        """
        Récupère les statistiques du cache
        
        Returns:
            dict: Statistiques du cache
        """
        if not self.is_available():
            return {
                'enabled': False,
                'connected': False,
                'keys_count': 0,
                'memory_usage': 0
            }
        
        try:
            info = self.redis_client.info()
            keys_count = self.redis_client.dbsize()
            
            return {
                'enabled': True,
                'connected': True,
                'keys_count': keys_count,
                'memory_usage': info.get('used_memory_human', '0B'),
                'redis_version': info.get('redis_version', 'Unknown'),
                'uptime': info.get('uptime_in_seconds', 0)
            }
        except Exception as e:
            print(f"Erreur statistiques cache: {e}")
            return {
                'enabled': True,
                'connected': False,
                'keys_count': 0,
                'memory_usage': '0B'
            }
    
    def health_check(self) -> Dict:
        """
        Vérification de santé du cache
        
        Returns:
            dict: État de santé du cache
        """
        if not self.cache_enabled:
            return {
                'status': 'disabled',
                'message': 'Cache désactivé'
            }
        
        if not self.is_available():
            return {
                'status': 'error',
                'message': 'Cache Redis non disponible'
            }
        
        try:
            # Test de connexion
            self.redis_client.ping()
            
            # Test d'écriture/lecture
            test_key = "agrobiz:health_check"
            test_value = {"test": "data", "timestamp": datetime.now().isoformat()}
            
            self.set(test_key, test_value, ttl=60)
            retrieved_value = self.get(test_key)
            
            if retrieved_value and retrieved_value.get('test') == 'data':
                return {
                    'status': 'healthy',
                    'message': 'Cache opérationnel',
                    'stats': self.get_cache_stats()
                }
            else:
                return {
                    'status': 'warning',
                    'message': 'Cache partiellement fonctionnel'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur cache: {str(e)}'
            } 