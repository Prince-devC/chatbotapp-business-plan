"""
Configuration centralisée pour AgroBiz Chatbot
Gère les variables d'environnement sur toutes les plateformes
"""

import os
from typing import Optional

class Config:
    """Configuration de base"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Base de données
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    
    # Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Twilio WhatsApp
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '5'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))  # 1 heure
    
    # File Storage
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16 * 1024 * 1024'))  # 16MB
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate_required_keys(cls) -> list:
        """Valide que toutes les clés requises sont configurées"""
        required_keys = [
            'GEMINI_API_KEY',
            'TWILIO_ACCOUNT_SID',
            'TWILIO_AUTH_TOKEN',
            'TWILIO_PHONE_NUMBER'
        ]
        
        missing_keys = []
        for key in required_keys:
            if not getattr(cls, key):
                missing_keys.append(key)
        
        return missing_keys
    
    @classmethod
    def get_platform_info(cls) -> dict:
        """Retourne des informations sur la plateforme de déploiement"""
        platform_info = {
            'platform': 'unknown',
            'database_type': 'sqlite',
            'has_ssl': False,
            'is_production': cls.FLASK_ENV == 'production'
        }
        
        # Détecter la plateforme
        if 'DATABASE_URL' in os.environ:
            if 'postgresql://' in cls.DATABASE_URL or 'postgres://' in cls.DATABASE_URL:
                platform_info['database_type'] = 'postgresql'
                
                if 'render.com' in cls.DATABASE_URL:
                    platform_info['platform'] = 'render'
                    platform_info['has_ssl'] = True
                elif 'herokuapp.com' in cls.DATABASE_URL:
                    platform_info['platform'] = 'heroku'
                    platform_info['has_ssl'] = True
                elif 'vercel.app' in cls.DATABASE_URL:
                    platform_info['platform'] = 'vercel'
                    platform_info['has_ssl'] = True
        
        return platform_info

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def validate(cls) -> bool:
        """Valide la configuration de production"""
        missing_keys = cls.validate_required_keys()
        if missing_keys:
            print(f"❌ Variables d'environnement manquantes: {', '.join(missing_keys)}")
            return False
        return True

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: Optional[str] = None) -> Config:
    """Récupère la configuration appropriée"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

# Configuration actuelle
current_config = get_config()

# Validation en production
if current_config.FLASK_ENV == 'production':
    if not current_config.validate():
        print("❌ Configuration de production invalide!")
        print("Vérifiez vos variables d'environnement.")
        exit(1)
    
    print("✅ Configuration de production validée")
    platform_info = current_config.get_platform_info()
    print(f"🌐 Plateforme: {platform_info['platform']}")
    print(f"🗄️  Base de données: {platform_info['database_type']}")
    print(f"🔒 SSL: {'Oui' if platform_info['has_ssl'] else 'Non'}") 