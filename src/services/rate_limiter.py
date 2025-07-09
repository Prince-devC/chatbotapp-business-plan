import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        self.access_code = "join-mais-ai-generate"
        self.max_requests = 5
        self.data_file = self._get_data_file_path()
        self._load_data()
    
    def _get_data_file_path(self) -> str:
        """Retourne le chemin du fichier de données des utilisateurs."""
        project_root = Path(__file__).parent.parent.parent.resolve()
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        return str(data_dir / "rate_limit_data.json")
    
    def _load_data(self):
        """Charge les données des utilisateurs depuis le fichier."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.users_data = json.load(f)
            else:
                self.users_data = {}
        except Exception as e:
            logger.error(f"Erreur chargement données rate limit: {str(e)}")
            self.users_data = {}
    
    def _save_data(self):
        """Sauvegarde les données des utilisateurs dans le fichier."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.users_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde données rate limit: {str(e)}")
    
    def get_user_data(self, user_id: str) -> Dict:
        """Récupère les données d'un utilisateur."""
        if user_id not in self.users_data:
            self.users_data[user_id] = {
                'requests_count': 0,
                'is_unlocked': False,
                'first_request': datetime.now().isoformat(),
                'last_request': None,
                'unlock_date': None
            }
        return self.users_data[user_id]
    
    def can_make_request(self, user_id: str) -> Tuple[bool, str]:
        """
        Vérifie si un utilisateur peut faire une requête.
        Retourne (peut_faire_requête, message)
        """
        user_data = self.get_user_data(user_id)
        
        # Si l'utilisateur est débloqué, il peut faire des requêtes illimitées
        if user_data.get('is_unlocked', False):
            return True, "Utilisateur débloqué"
        
        # Vérifier la limite de 5 requêtes
        if user_data['requests_count'] >= self.max_requests:
            return False, f"Limite atteinte ({self.max_requests} requêtes). Utilisez le code '{self.access_code}' pour continuer."
        
        return True, f"Requêtes restantes: {self.max_requests - user_data['requests_count']}"
    
    def increment_request(self, user_id: str):
        """Incrémente le compteur de requêtes d'un utilisateur."""
        user_data = self.get_user_data(user_id)
        user_data['requests_count'] += 1
        user_data['last_request'] = datetime.now().isoformat()
        self._save_data()
        logger.info(f"Requête incrémentée pour {user_id}: {user_data['requests_count']}/{self.max_requests}")
    
    def unlock_user(self, user_id: str, code: str) -> Tuple[bool, str]:
        """
        Débloque un utilisateur avec le code d'accès.
        Retourne (succès, message)
        """
        if code != self.access_code:
            return False, f"Code incorrect. Le code correct est: {self.access_code}"
        
        user_data = self.get_user_data(user_id)
        user_data['is_unlocked'] = True
        user_data['unlock_date'] = datetime.now().isoformat()
        self._save_data()
        
        logger.info(f"Utilisateur {user_id} débloqué avec succès")
        return True, "✅ Compte débloqué ! Vous pouvez maintenant utiliser le service sans limite."
    
    def get_user_status(self, user_id: str) -> Dict:
        """Retourne le statut complet d'un utilisateur."""
        user_data = self.get_user_data(user_id)
        can_request, message = self.can_make_request(user_id)
        
        return {
            'user_id': user_id,
            'requests_count': user_data['requests_count'],
            'is_unlocked': user_data.get('is_unlocked', False),
            'can_make_request': can_request,
            'message': message,
            'max_requests': self.max_requests,
            'remaining_requests': max(0, self.max_requests - user_data['requests_count']),
            'first_request': user_data.get('first_request'),
            'last_request': user_data.get('last_request'),
            'unlock_date': user_data.get('unlock_date')
        }
    
    def reset_user(self, user_id: str):
        """Réinitialise les données d'un utilisateur (pour les tests)."""
        if user_id in self.users_data:
            del self.users_data[user_id]
            self._save_data()
            logger.info(f"Utilisateur {user_id} réinitialisé")

# Instance globale du rate limiter
rate_limiter = RateLimiter() 