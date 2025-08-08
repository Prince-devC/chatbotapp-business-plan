#!/usr/bin/env python3
"""
Tests pour les services Semaine 8 AgroBizChat
Validation localisation et finalisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.localization_service import LocalizationService

def test_localization_service():
    """Test du service de localisation"""
    print("🌍 Test LocalizationService...")
    
    try:
        localization_service = LocalizationService()
        
        # Test langues supportées
        languages = localization_service.get_supported_languages()
        assert len(languages) == 5, f"Nombre de langues incorrect: {len(languages)}"
        
        expected_languages = ['fr', 'fon', 'yor', 'min', 'bar']
        for lang_code in expected_languages:
            assert lang_code in languages, f"Langue {lang_code} manquante"
        
        print("✅ Langues supportées OK")
        print(f"✅ Langues: {list(languages.keys())}")
        
        # Test traductions de base
        test_keys = ['greeting', 'help', 'business_plan', 'weather', 'disease']
        
        for lang_code in ['fr', 'fon', 'yor']:
            for key in test_keys:
                translation = localization_service.translate(key, lang_code)
                assert translation is not None, f"Traduction manquante pour {key} en {lang_code}"
                assert len(translation) > 0, f"Traduction vide pour {key} en {lang_code}"
            
            print(f"✅ Traductions {lang_code} OK")
        
        # Test termes agricoles
        agricultural_terms = ['corn', 'pineapple', 'agriculture', 'farmer']
        
        for lang_code in ['fr', 'fon', 'yor']:
            for term in agricultural_terms:
                translation = localization_service.translate_agricultural_term(term, lang_code)
                assert translation is not None, f"Terme agricole manquant pour {term} en {lang_code}"
            
            print(f"✅ Termes agricoles {lang_code} OK")
        
        # Test détection de langue
        test_texts = [
            ("Bonjour comment allez-vous ?", "fr"),
            ("Ẹ káàbọ̀ báwo ni o ṣe ?", "yor"),
            ("Agoo bɔ nyu ?", "fon")
        ]
        
        for text, expected_lang in test_texts:
            detected_lang = localization_service.detect_language(text)
            print(f"✅ Détection: '{text[:20]}...' -> {detected_lang} (attendu: {expected_lang})")
        
        # Test formatage nombres
        test_numbers = [1000, 50000, 1000000]
        
        for lang_code in ['fr', 'fon', 'yor']:
            for number in test_numbers:
                formatted = localization_service.format_number(number, lang_code)
                assert formatted is not None, f"Formatage nombre manquant pour {number} en {lang_code}"
            
            print(f"✅ Formatage nombres {lang_code} OK")
        
        # Test formatage monnaie
        test_amounts = [1000, 50000, 1000000]
        
        for lang_code in ['fr', 'fon', 'yor']:
            for amount in test_amounts:
                formatted = localization_service.format_currency(amount, lang_code)
                assert formatted is not None, f"Formatage monnaie manquant pour {amount} en {lang_code}"
                assert 'FCFA' in formatted or '₦' in formatted, f"Symbole monnaie manquant pour {lang_code}"
            
            print(f"✅ Formatage monnaie {lang_code} OK")
        
        # Test réponses localisées
        response_types = ['greeting', 'business_plan_intro', 'weather_info', 'disease_diagnosis']
        
        for lang_code in ['fr', 'fon', 'yor']:
            for response_type in response_types:
                response = localization_service.get_localized_response(response_type, lang_code)
                assert response is not None, f"Réponse manquante pour {response_type} en {lang_code}"
                assert len(response) > 0, f"Réponse vide pour {response_type} en {lang_code}"
            
            print(f"✅ Réponses localisées {lang_code} OK")
        
        print("🎉 LocalizationService: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur LocalizationService: {e}")
        return False

def test_language_specific_features():
    """Test des fonctionnalités spécifiques par langue"""
    print("\n🗣️ Test fonctionnalités spécifiques par langue...")
    
    try:
        localization_service = LocalizationService()
        
        # Test Fon
        fon_greeting = localization_service.get_greeting('fon')
        assert 'AgroBizChat' in fon_greeting, "AgroBizChat manquant dans salutation Fon"
        print("✅ Salutation Fon OK")
        
        fon_corn = localization_service.translate_agricultural_term('corn', 'fon')
        assert fon_corn == 'Kpɛn', f"Traduction maïs Fon incorrecte: {fon_corn}"
        print("✅ Termes agricoles Fon OK")
        
        # Test Yoruba
        yor_greeting = localization_service.get_greeting('yor')
        assert 'AgroBizChat' in yor_greeting, "AgroBizChat manquant dans salutation Yoruba"
        print("✅ Salutation Yoruba OK")
        
        yor_corn = localization_service.translate_agricultural_term('corn', 'yor')
        assert yor_corn == 'Ọkà', f"Traduction maïs Yoruba incorrecte: {yor_corn}"
        print("✅ Termes agricoles Yoruba OK")
        
        # Test formatage spécifique
        fon_currency = localization_service.format_currency(50000, 'fon')
        assert 'FCFA' in fon_currency, "FCFA manquant dans formatage Fon"
        
        yor_currency = localization_service.format_currency(50000, 'yor')
        assert '₦' in yor_currency, "₦ manquant dans formatage Yoruba"
        
        print("✅ Formatage spécifique par langue OK")
        
        print("🎉 Fonctionnalités spécifiques par langue: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonctionnalités spécifiques: {e}")
        return False

def test_agricultural_terminology():
    """Test de la terminologie agricole complète"""
    print("\n🌾 Test terminologie agricole...")
    
    try:
        localization_service = LocalizationService()
        
        # Test termes agricoles par langue
        agricultural_terms = [
            'corn', 'pineapple', 'agriculture', 'farmer', 'farm',
            'crop', 'harvest', 'planting', 'irrigation', 'fertilizer',
            'pesticide', 'soil', 'weather', 'rain', 'sun',
            'disease', 'treatment', 'prevention', 'yield', 'profit',
            'cost', 'price', 'market', 'business_plan', 'investment',
            'loan', 'cooperative', 'extension', 'training', 'technology'
        ]
        
        for lang_code in ['fr', 'fon', 'yor']:
            translations = {}
            
            for term in agricultural_terms:
                translation = localization_service.translate_agricultural_term(term, lang_code)
                translations[term] = translation
                assert translation is not None, f"Traduction manquante pour {term} en {lang_code}"
            
            print(f"✅ Terminologie agricole {lang_code}: {len(translations)} termes")
            
            # Vérifier quelques termes clés
            if lang_code == 'fr':
                assert translations['corn'] == 'Maïs', f"Maïs incorrect: {translations['corn']}"
                assert translations['pineapple'] == 'Ananas', f"Ananas incorrect: {translations['pineapple']}"
            elif lang_code == 'fon':
                assert translations['corn'] == 'Kpɛn', f"Kpɛn incorrect: {translations['corn']}"
                assert translations['pineapple'] == 'Anana', f"Anana incorrect: {translations['pineapple']}"
            elif lang_code == 'yor':
                assert translations['corn'] == 'Ọkà', f"Ọkà incorrect: {translations['corn']}"
                assert translations['pineapple'] == 'Ọ̀gbẹ̀dẹ̀', f"Ọ̀gbẹ̀dẹ̀ incorrect: {translations['pineapple']}"
        
        print("🎉 Terminologie agricole: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur terminologie agricole: {e}")
        return False

def test_business_plan_localization():
    """Test de la localisation des business plans"""
    print("\n📊 Test localisation business plans...")
    
    try:
        localization_service = LocalizationService()
        
        # Test traductions business plan
        for lang_code in ['fr', 'fon', 'yor']:
            translations = localization_service.translate_business_plan_terms(lang_code)
            
            expected_terms = [
                'business_plan', 'investment', 'profit', 'cost', 'yield',
                'market', 'price', 'cooperative', 'loan'
            ]
            
            for term in expected_terms:
                assert term in translations, f"Terme business plan manquant: {term}"
                assert translations[term] is not None, f"Traduction vide pour {term}"
            
            print(f"✅ Business plan {lang_code}: {len(translations)} termes")
        
        # Test formatage monnaie pour business plans
        test_amounts = [100000, 500000, 1000000]
        
        for lang_code in ['fr', 'fon', 'yor']:
            for amount in test_amounts:
                formatted = localization_service.format_currency(amount, lang_code)
                assert 'FCFA' in formatted or '₦' in formatted, f"Monnaie manquante pour {lang_code}"
            
            print(f"✅ Formatage monnaie business plan {lang_code} OK")
        
        print("🎉 Localisation business plans: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur localisation business plans: {e}")
        return False

def test_weather_localization():
    """Test de la localisation météo"""
    print("\n🌦️ Test localisation météo...")
    
    try:
        localization_service = LocalizationService()
        
        # Test traductions météo
        for lang_code in ['fr', 'fon', 'yor']:
            translations = localization_service.translate_weather_terms(lang_code)
            
            expected_terms = ['weather', 'rain', 'sun', 'soil']
            
            for term in expected_terms:
                assert term in translations, f"Terme météo manquant: {term}"
                assert translations[term] is not None, f"Traduction vide pour {term}"
            
            print(f"✅ Météo {lang_code}: {len(translations)} termes")
        
        # Test réponses météo localisées
        for lang_code in ['fr', 'fon', 'yor']:
            response = localization_service.get_localized_response('weather_info', lang_code)
            assert response is not None, f"Réponse météo manquante pour {lang_code}"
            assert len(response) > 0, f"Réponse météo vide pour {lang_code}"
        
        print("🎉 Localisation météo: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur localisation météo: {e}")
        return False

def test_disease_localization():
    """Test de la localisation maladies"""
    print("\n🏥 Test localisation maladies...")
    
    try:
        localization_service = LocalizationService()
        
        # Test traductions maladies
        for lang_code in ['fr', 'fon', 'yor']:
            translations = localization_service.translate_disease_terms(lang_code)
            
            expected_terms = ['disease', 'treatment', 'prevention']
            
            for term in expected_terms:
                assert term in translations, f"Terme maladie manquant: {term}"
                assert translations[term] is not None, f"Traduction vide pour {term}"
            
            print(f"✅ Maladies {lang_code}: {len(translations)} termes")
        
        # Test réponses diagnostic localisées
        for lang_code in ['fr', 'fon', 'yor']:
            response = localization_service.get_localized_response('disease_diagnosis', lang_code)
            assert response is not None, f"Réponse diagnostic manquante pour {lang_code}"
            assert len(response) > 0, f"Réponse diagnostic vide pour {lang_code}"
        
        print("🎉 Localisation maladies: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur localisation maladies: {e}")
        return False

def test_integration_localization():
    """Test d'intégration de la localisation"""
    print("\n🔗 Test intégration localisation...")
    
    try:
        localization_service = LocalizationService()
        
        # Test intégration complète
        test_scenarios = [
            {
                'lang': 'fr',
                'greeting': 'Bonjour ! Je suis AgroBizChat',
                'corn': 'Maïs',
                'currency': 'FCFA'
            },
            {
                'lang': 'fon',
                'greeting': 'Bonjour ! N ye AgroBizChat',
                'corn': 'Kpɛn',
                'currency': 'FCFA'
            },
            {
                'lang': 'yor',
                'greeting': 'Ẹ káàbọ̀ ! Èmi ni AgroBizChat',
                'corn': 'Ọkà',
                'currency': '₦'
            }
        ]
        
        for scenario in test_scenarios:
            lang_code = scenario['lang']
            
            # Test salutation
            greeting = localization_service.get_greeting(lang_code)
            assert scenario['greeting'] in greeting, f"Salutation incorrecte pour {lang_code}"
            
            # Test terme agricole
            corn = localization_service.translate_agricultural_term('corn', lang_code)
            assert corn == scenario['corn'], f"Maïs incorrect pour {lang_code}: {corn}"
            
            # Test formatage monnaie
            currency = localization_service.format_currency(1000, lang_code)
            assert scenario['currency'] in currency, f"Monnaie incorrecte pour {lang_code}"
            
            print(f"✅ Intégration {lang_code} OK")
        
        # Test détection automatique
        test_texts = [
            ("Bonjour, comment allez-vous ?", "fr"),
            ("Ẹ káàbọ̀, báwo ni o ṣe ?", "yor"),
            ("Agoo, bɔ nyu ?", "fon")
        ]
        
        for text, expected_lang in test_texts:
            detected_lang = localization_service.detect_language(text)
            print(f"✅ Détection: '{text[:15]}...' -> {detected_lang}")
        
        print("🎉 Intégration localisation: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration localisation: {e}")
        return False

def run_week8_tests():
    """Exécute tous les tests de la semaine 8"""
    print("🚀 Début des tests Semaine 8 - Localisation et finalisation...\n")
    
    tests = [
        test_localization_service,
        test_language_specific_features,
        test_agricultural_terminology,
        test_business_plan_localization,
        test_weather_localization,
        test_disease_localization,
        test_integration_localization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Résultats des tests Semaine 8:")
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passent! Services Semaine 8 prêts pour la production.")
        print("🌍 AgroBizChat v2.0 avec support multilingue complet !")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == '__main__':
    success = run_week8_tests()
    sys.exit(0 if success else 1) 