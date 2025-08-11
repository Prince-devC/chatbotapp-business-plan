#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration de déploiement
Usage: python test_deployment.py
"""

import os
import sys
import requests
from pathlib import Path

def test_environment_variables():
    """Teste les variables d'environnement requises"""
    print("🔍 Test des variables d'environnement...")
    
    required_vars = [
        'GEMINI_API_KEY',
        'TWILIO_ACCOUNT_SID', 
        'TWILIO_AUTH_TOKEN',
        'TWILIO_PHONE_NUMBER'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * min(len(value), 8)}...")
        else:
            print(f"❌ {var}: MANQUANT")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Variables manquantes: {', '.join(missing_vars)}")
        print("Configurez ces variables avant le déploiement")
        return False
    
    print("✅ Toutes les variables requises sont configurées")
    return True

def test_dependencies():
    """Teste les dépendances Python"""
    print("\n📦 Test des dépendances...")
    
    required_packages = [
        'flask',
        'gunicorn',
        'psycopg2-binary',
        'twilio',
        'google-generativeai'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}: MANQUANT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Packages manquants: {', '.join(missing_packages)}")
        print("Installez-les avec: pip install -r requirements.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def test_file_structure():
    """Teste la structure des fichiers"""
    print("\n📁 Test de la structure des fichiers...")
    
    required_files = [
        'src/main.py',
        'requirements.txt',
        'render.yaml',
        'vercel.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}: MANQUANT")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    print("✅ Structure des fichiers correcte")
    return True

def test_database_connection():
    """Teste la connexion à la base de données"""
    print("\n🗄️  Test de la base de données...")
    
    try:
        from src.models.database import get_db_connection
        conn = get_db_connection()
        conn.close()
        print("✅ Connexion à la base de données réussie")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def test_webhook_endpoints():
    """Teste les endpoints de webhook"""
    print("\n🌐 Test des endpoints de webhook...")
    
    # Test local si Flask est en cours d'exécution
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Serveur Flask local accessible")
            return True
        else:
            print(f"⚠️  Serveur accessible mais statut: {response.status_code}")
            return True
    except requests.exceptions.ConnectionError:
        print("ℹ️  Serveur Flask local non accessible (normal si pas démarré)")
        return True
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test de configuration pour le déploiement")
    print("=" * 50)
    
    tests = [
        test_environment_variables,
        test_dependencies,
        test_file_structure,
        test_database_connection,
        test_webhook_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur lors du test {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés! Prêt pour le déploiement.")
        print("\n🚀 Pour déployer:")
        print("1. ./deploy.sh (choix de plateforme)")
        print("2. Ou directement: ./deploy_render.sh")
        return True
    else:
        print("⚠️  Certains tests ont échoué. Corrigez les problèmes avant le déploiement.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 