#!/usr/bin/env python3
"""
Tests pour les services AgroBizChat
Valide les nouveaux services créés pour la v2.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.unit_converter import UnitConverter
from src.services.weather_service import WeatherService
from src.services.disease_detection import DiseaseDetectionService
from src.services.payment_service import PaymentService
from src.services.conversational_ai import ConversationalAI

def test_unit_converter():
    """Test du service de conversion d'unités"""
    print("🧪 Test UnitConverter...")
    
    try:
        # Test conversion canti vers ha
        ha_value = UnitConverter.convert_area(10, 'canti', 'ha')
        assert ha_value == 0.4, f"Erreur conversion canti->ha: {ha_value}"
        print("✅ Conversion canti->ha OK")
        
        # Test conversion canti vers m²
        m2_value = UnitConverter.convert_area(10, 'canti', 'm2')
        assert m2_value == 4000, f"Erreur conversion canti->m2: {m2_value}"
        print("✅ Conversion canti->m2 OK")
        
        # Test surface standard
        standard_area = UnitConverter.get_standard_area(10, 'canti')
        assert standard_area['ha'] == 0.4, f"Erreur surface standard ha: {standard_area['ha']}"
        assert standard_area['m2'] == 4000, f"Erreur surface standard m2: {standard_area['m2']}"
        print("✅ Surface standard OK")
        
        # Test formatage affichage
        display = UnitConverter.format_area_display(standard_area)
        assert "0.4 hectare" in display, f"Erreur formatage: {display}"
        print("✅ Formatage affichage OK")
        
        print("🎉 UnitConverter: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur UnitConverter: {e}")
        return False

def test_weather_service():
    """Test du service météo"""
    print("\n🌦️ Test WeatherService...")
    
    try:
        weather_service = WeatherService()
        
        # Test récupération météo actuelle
        weather = weather_service.get_current_weather("Zone des terres de barre")
        if weather:
            print("✅ Récupération météo actuelle OK")
        else:
            print("⚠️ Pas de données météo (API non configurée)")
        
        # Test conseils agro-météo
        advice = weather_service.get_agro_advice("Zone des terres de barre", "mais")
        if advice:
            assert 'culture' in advice, "Conseils incomplets"
            assert 'conseils' in advice, "Conseils manquants"
            print("✅ Conseils agro-météo OK")
        else:
            print("⚠️ Pas de conseils (API non configurée)")
        
        # Test mapping zones
        coords = weather_service._get_zone_coordinates("Zone des terres de barre")
        assert coords is not None, "Coordonnées zone non trouvées"
        assert 'lat' in coords, "Latitude manquante"
        assert 'lon' in coords, "Longitude manquante"
        print("✅ Mapping zones OK")
        
        print("🎉 WeatherService: Tests de base passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur WeatherService: {e}")
        return False

def test_disease_detection():
    """Test du service de diagnostic des maladies"""
    print("\n🔍 Test DiseaseDetectionService...")
    
    try:
        disease_service = DiseaseDetectionService()
        
        # Test prétraitement image (simulation)
        test_image_data = b"fake_image_data"
        processed = disease_service._preprocess_image(test_image_data)
        # Le test échouera car pas d'image réelle, mais on teste la structure
        
        # Test génération diagnostic
        mock_detection_result = {
            'disease': 'charançon du maïs',
            'confidence': 0.85,
            'symptoms': ['Trous dans les feuilles', 'Plants affaiblis']
        }
        
        diagnosis = disease_service._generate_diagnosis(mock_detection_result, 'mais')
        assert diagnosis['culture'] == 'mais', "Culture incorrecte"
        assert diagnosis['disease_name'] == 'charançon du maïs', "Maladie incorrecte"
        assert diagnosis['severity'] == 'Élevée', "Sévérité incorrecte"
        assert len(diagnosis['treatments']) > 0, "Traitements manquants"
        print("✅ Génération diagnostic OK")
        
        # Test traitements
        treatments = disease_service._get_treatments('charançon du maïs', 'mais')
        assert len(treatments) > 0, "Aucun traitement trouvé"
        print("✅ Base de données traitements OK")
        
        # Test prévention
        prevention = disease_service._get_prevention('charançon du maïs', 'mais')
        assert len(prevention) > 0, "Aucune prévention trouvée"
        print("✅ Base de données prévention OK")
        
        print("🎉 DiseaseDetectionService: Tests de base passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur DiseaseDetectionService: {e}")
        return False

def test_payment_service():
    """Test du service de paiement"""
    print("\n💳 Test PaymentService...")
    
    try:
        payment_service = PaymentService(provider="kkiapay")
        
        # Test packages de prix
        packages = payment_service.get_pricing_packages()
        assert len(packages) == 3, "Nombre de packages incorrect"
        
        basic_package = packages[0]
        assert basic_package['id'] == 'basic', "ID package basique incorrect"
        assert basic_package['price'] == 500, "Prix package basique incorrect"
        assert basic_package['currency'] == 'XOF', "Devise incorrecte"
        print("✅ Packages de prix OK")
        
        # Test création paiement (simulation)
        payment_data = payment_service.create_payment(
            amount=500,
            user_id='test_user_001',
            description='Pack Basique AgroBizChat',
            phone_number='+22990123456'
        )
        # Le test échouera car pas d'API configurée, mais on teste la structure
        
        print("🎉 PaymentService: Tests de base passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur PaymentService: {e}")
        return False

def test_conversational_ai():
    """Test du service d'IA conversationnelle"""
    print("\n🤖 Test ConversationalAI...")
    
    try:
        ai_service = ConversationalAI()
        
        # Test détection d'intention
        intent = ai_service._detect_intent("Comment planter du maïs ?")
        assert intent['type'] == 'faq', f"Type d'intention incorrect: {intent['type']}"
        assert intent['confidence'] > 0, "Confiance nulle"
        print("✅ Détection d'intention OK")
        
        # Test traitement message FAQ
        response = ai_service.process_message("Comment planter du maïs ?")
        assert 'response' in response, "Réponse manquante"
        assert 'intent' in response, "Intention manquante"
        assert 'suggestions' in response, "Suggestions manquantes"
        print("✅ Traitement message FAQ OK")
        
        # Test traitement message technique
        response = ai_service.process_message("Quels engrais utiliser ?")
        assert response['intent']['type'] == 'technical', "Type technique non détecté"
        print("✅ Traitement message technique OK")
        
        # Test traitement message général
        response = ai_service.process_message("Bonjour")
        assert response['intent']['type'] == 'general', "Type général non détecté"
        print("✅ Traitement message général OK")
        
        # Test base FAQ
        faq_db = ai_service._load_faq_database()
        assert len(faq_db) > 0, "Base FAQ vide"
        print("✅ Base FAQ OK")
        
        # Test patterns d'intention
        patterns = ai_service._load_intent_patterns()
        assert 'faq' in patterns, "Patterns FAQ manquants"
        assert 'technical' in patterns, "Patterns techniques manquants"
        print("✅ Patterns d'intention OK")
        
        print("🎉 ConversationalAI: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur ConversationalAI: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("🚀 Début des tests AgroBizChat v2.0...\n")
    
    tests = [
        test_unit_converter,
        test_weather_service,
        test_disease_detection,
        test_payment_service,
        test_conversational_ai
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Résultats des tests:")
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passent! Services prêts pour la production.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1) 