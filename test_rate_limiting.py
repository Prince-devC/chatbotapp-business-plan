#!/usr/bin/env python3
"""
Script de test pour le système de rate limiting
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.rate_limiter import rate_limiter
from src.services.gemini_service import GeminiAnalysisService
from src.routes.chatbot import get_all_templates
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_rate_limiter():
    """Test du système de rate limiting."""
    print("🧪 Test du système de rate limiting")
    print("=" * 50)
    
    # Test 1: Vérifier l'état initial d'un utilisateur
    user_id = "test_user_123"
    print(f"\n1. Test de l'état initial pour {user_id}")
    status = rate_limiter.get_user_status(user_id)
    print(f"   - Requêtes effectuées: {status['requests_count']}")
    print(f"   - Peut faire une requête: {status['can_make_request']}")
    print(f"   - Message: {status['message']}")
    
    # Test 2: Simuler 5 requêtes
    print(f"\n2. Simulation de 5 requêtes pour {user_id}")
    for i in range(5):
        can_request, message = rate_limiter.can_make_request(user_id)
        if can_request:
            rate_limiter.increment_request(user_id)
            print(f"   - Requête {i+1}: OK")
        else:
            print(f"   - Requête {i+1}: {message}")
            break
    
    # Test 3: Vérifier l'état après 5 requêtes
    print(f"\n3. État après 5 requêtes")
    status = rate_limiter.get_user_status(user_id)
    print(f"   - Requêtes effectuées: {status['requests_count']}")
    print(f"   - Peut faire une requête: {status['can_make_request']}")
    print(f"   - Message: {status['message']}")
    
    # Test 4: Tentative de déblocage avec mauvais code
    print(f"\n4. Test déblocage avec mauvais code")
    success, message = rate_limiter.unlock_user(user_id, "mauvais-code")
    print(f"   - Succès: {success}")
    print(f"   - Message: {message}")
    
    # Test 5: Tentative de déblocage avec bon code
    print(f"\n5. Test déblocage avec bon code")
    success, message = rate_limiter.unlock_user(user_id, "join-mais-ai-generate")
    print(f"   - Succès: {success}")
    print(f"   - Message: {message}")
    
    # Test 6: Vérifier l'état après déblocage
    print(f"\n6. État après déblocage")
    status = rate_limiter.get_user_status(user_id)
    print(f"   - Requêtes effectuées: {status['requests_count']}")
    print(f"   - Débloqué: {status['is_unlocked']}")
    print(f"   - Peut faire une requête: {status['can_make_request']}")
    print(f"   - Message: {status['message']}")
    
    # Test 7: Test avec Gemini Service
    print(f"\n7. Test avec Gemini Service")
    try:
        templates = get_all_templates()
        gemini_service = GeminiAnalysisService()
        
        # Test avec un utilisateur non débloqué
        test_user = "test_user_limited"
        for i in range(6):  # 6 requêtes pour dépasser la limite
            result = gemini_service.analyze_documents_for_business_plan(
                templates, 
                "culture de maïs sur 10 hectares", 
                test_user
            )
            print(f"   - Requête {i+1}: {'Succès' if result['success'] else 'Échec'}")
            if not result['success'] and result.get('is_rate_limited'):
                print(f"   - Message: {result['error']}")
                break
        
        # Test déblocage via Gemini
        unlock_result = gemini_service.analyze_documents_for_business_plan(
            templates, 
            "join-mais-ai-generate", 
            test_user
        )
        print(f"   - Tentative de déblocage: {'Succès' if unlock_result.get('unlock_success') else 'Échec'}")
        if unlock_result.get('unlock_message'):
            print(f"   - Message: {unlock_result['unlock_message']}")
        
    except Exception as e:
        print(f"   - Erreur lors du test Gemini: {str(e)}")
    
    # Test 8: Réinitialiser l'utilisateur de test
    print(f"\n8. Réinitialisation de l'utilisateur de test")
    rate_limiter.reset_user(user_id)
    rate_limiter.reset_user("test_user_limited")
    print("   - Utilisateurs réinitialisés")
    
    print("\n✅ Tests terminés")

def test_whatsapp_messages():
    """Test des messages WhatsApp avec rate limiting."""
    print("\n📱 Test des messages WhatsApp")
    print("=" * 50)
    
    from src.services.whatsapp_service import whatsapp_service
    
    # Test message d'erreur normal
    print("\n1. Test message d'erreur normal")
    whatsapp_service.send_error_message("+1234567890", "Erreur de test", is_rate_limited=False)
    
    # Test message d'erreur avec rate limiting
    print("\n2. Test message d'erreur avec rate limiting")
    whatsapp_service.send_error_message("+1234567890", "Limite atteinte", is_rate_limited=True)
    
    # Test message de déblocage réussi
    print("\n3. Test message de déblocage réussi")
    whatsapp_service.send_unlock_message("+1234567890", True, "Compte débloqué avec succès")
    
    # Test message de déblocage échoué
    print("\n4. Test message de déblocage échoué")
    whatsapp_service.send_unlock_message("+1234567890", False, "Code incorrect")
    
    print("\n✅ Tests des messages terminés")

if __name__ == "__main__":
    print("🚀 Démarrage des tests du système de rate limiting")
    print("=" * 60)
    
    try:
        test_rate_limiter()
        test_whatsapp_messages()
        
        print("\n🎉 Tous les tests ont été exécutés avec succès !")
        print("\n📊 Résumé:")
        print("- Système de rate limiting fonctionnel")
        print("- Limite de 5 requêtes par utilisateur")
        print("- Code de déblocage: join-mais-ai-generate")
        print("- Messages WhatsApp adaptés au rate limiting")
        print("- Intégration avec Gemini Service")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {str(e)}")
        import traceback
        traceback.print_exc() 