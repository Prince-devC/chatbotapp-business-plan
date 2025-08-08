#!/usr/bin/env python3
"""
Tests pour les services Semaine 5 AgroBizChat
Validation IA conversationnelle et détection d'intention
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.conversational_ai import ConversationalAI

def test_conversational_ai_service():
    """Test du service d'IA conversationnelle"""
    print("🧠 Test ConversationalAI...")
    
    try:
        conversational_ai = ConversationalAI()
        
        # Test chargement des données
        assert len(conversational_ai.intents) > 0, "Intents non chargés"
        assert len(conversational_ai.faq_data) > 0, "FAQ non chargée"
        assert len(conversational_ai.scenarios) > 0, "Scénarios non chargés"
        
        print("✅ Données chargées OK")
        print(f"✅ Intents: {len(conversational_ai.intents)}")
        print(f"✅ FAQ: {len(conversational_ai.faq_data)}")
        print(f"✅ Scénarios: {len(conversational_ai.scenarios)}")
        
        # Test normalisation des messages
        test_messages = [
            "Bonjour !",
            "COMMENT ALLEZ-VOUS?",
            "Salut...",
            "  bonjour  "
        ]
        
        for message in test_messages:
            normalized = conversational_ai._normalize_message(message)
            assert len(normalized) > 0, f"Normalisation échouée pour: {message}"
            assert normalized.islower(), f"Normalisation non en minuscules: {normalized}"
        
        print("✅ Normalisation des messages OK")
        
        # Test détection d'intention
        test_intents = [
            ("bonjour", "greeting"),
            ("salut", "greeting"),
            ("business plan", "business_plan"),
            ("météo", "weather"),
            ("maladie", "disease_diagnosis"),
            ("paiement", "payment"),
            ("aide", "help"),
            ("au revoir", "goodbye")
        ]
        
        for message, expected_intent in test_intents:
            intent, confidence = conversational_ai._detect_intent(message)
            assert intent == expected_intent, f"Intention incorrecte pour '{message}': {intent} != {expected_intent}"
            assert confidence > 0, f"Confiance nulle pour '{message}'"
        
        print("✅ Détection d'intention OK")
        
        # Test FAQ
        test_faq = [
            ("comment créer un business plan", "business_plan"),
            ("conseils météo", "weather_advice"),
            ("maladies des plantes", "disease_management"),
            ("tarifs", "payment_info")
        ]
        
        for message, expected_category in test_faq:
            faq_match = conversational_ai._check_faq(message)
            if faq_match:
                assert faq_match['category'] == expected_category, f"FAQ incorrecte pour '{message}'"
                print(f"✅ FAQ '{expected_category}' détectée")
            else:
                print(f"⚠️ FAQ non détectée pour '{message}'")
        
        # Test scénarios
        test_scenarios = [
            ("plantation maïs", "mais_plantation"),
            ("récolte maïs", "mais_recolte"),
            ("pesticide", "pesticide_application")
        ]
        
        for message, expected_scenario in test_scenarios:
            scenario_match = conversational_ai._check_scenarios(message)
            if scenario_match:
                assert scenario_match['scenario'] == expected_scenario, f"Scénario incorrect pour '{message}'"
                assert len(scenario_match['steps']) > 0, f"Pas d'étapes pour le scénario '{expected_scenario}'"
                print(f"✅ Scénario '{expected_scenario}' détecté")
            else:
                print(f"⚠️ Scénario non détecté pour '{message}'")
        
        print("🎉 ConversationalAI: Tests de base passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur ConversationalAI: {e}")
        return False

def test_message_processing():
    """Test du traitement des messages"""
    print("\n💬 Test traitement des messages...")
    
    try:
        conversational_ai = ConversationalAI()
        
        # Test messages avec réponses attendues
        test_cases = [
            {
                'message': 'bonjour',
                'expected_intent': 'greeting',
                'expected_confidence': 0.5
            },
            {
                'message': 'je veux créer un business plan',
                'expected_intent': 'business_plan',
                'expected_confidence': 0.3
            },
            {
                'message': 'quelle est la météo',
                'expected_intent': 'weather',
                'expected_confidence': 0.3
            },
            {
                'message': 'ma plante est malade',
                'expected_intent': 'disease_diagnosis',
                'expected_confidence': 0.3
            },
            {
                'message': 'combien ça coûte',
                'expected_intent': 'payment',
                'expected_confidence': 0.3
            },
            {
                'message': 'aide moi',
                'expected_intent': 'help',
                'expected_confidence': 0.3
            }
        ]
        
        for test_case in test_cases:
            result = conversational_ai.process_message(
                message=test_case['message'],
                user_id='test_user_001'
            )
            
            assert 'response' in result, "Réponse manquante"
            assert 'intent' in result, "Intention manquante"
            assert 'confidence' in result, "Confiance manquante"
            assert 'actions' in result, "Actions manquantes"
            
            assert len(result['response']) > 0, "Réponse vide"
            assert result['intent'] == test_case['expected_intent'], f"Intention incorrecte: {result['intent']} != {test_case['expected_intent']}"
            assert result['confidence'] >= test_case['expected_confidence'], f"Confiance trop faible: {result['confidence']} < {test_case['expected_confidence']}"
            
            print(f"✅ Message '{test_case['message']}': {result['intent']} ({result['confidence']:.1%})")
        
        print("🎉 Traitement des messages: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur traitement messages: {e}")
        return False

def test_context_management():
    """Test de la gestion du contexte"""
    print("\n📝 Test gestion du contexte...")
    
    try:
        conversational_ai = ConversationalAI()
        user_id = 'test_context_user'
        
        # Test contexte vide
        context = conversational_ai.get_user_context(user_id)
        assert context == {}, "Contexte initial non vide"
        
        # Test mise à jour du contexte
        conversational_ai._update_context(user_id, 'greeting', 'bonjour')
        context = conversational_ai.get_user_context(user_id)
        
        assert context['last_intent'] == 'greeting', "Dernière intention incorrecte"
        assert context['last_message'] == 'bonjour', "Dernier message incorrect"
        assert len(context['conversation_history']) == 1, "Historique incorrect"
        
        # Test ajout d'un autre message
        conversational_ai._update_context(user_id, 'business_plan', 'business plan')
        context = conversational_ai.get_user_context(user_id)
        
        assert context['last_intent'] == 'business_plan', "Dernière intention non mise à jour"
        assert len(context['conversation_history']) == 2, "Historique non mis à jour"
        
        # Test effacement du contexte
        conversational_ai.clear_user_context(user_id)
        context = conversational_ai.get_user_context(user_id)
        assert context == {}, "Contexte non effacé"
        
        print("✅ Gestion du contexte OK")
        
        # Test actions suggérées
        actions = conversational_ai._get_actions('business_plan')
        assert 'create_business_plan' in actions, "Action create_business_plan manquante"
        
        actions = conversational_ai._get_actions('weather')
        assert 'get_weather' in actions, "Action get_weather manquante"
        
        actions = conversational_ai._get_actions('disease_diagnosis')
        assert 'request_photo' in actions, "Action request_photo manquante"
        
        print("✅ Actions suggérées OK")
        
        print("🎉 Gestion du contexte: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur gestion contexte: {e}")
        return False

def test_faq_and_scenarios():
    """Test des FAQ et scénarios"""
    print("\n📚 Test FAQ et scénarios...")
    
    try:
        conversational_ai = ConversationalAI()
        
        # Test FAQ
        faq_categories = ['business_plan', 'weather_advice', 'disease_management', 'payment_info']
        
        for category in faq_categories:
            faq_data = conversational_ai.faq_data[category]
            assert 'questions' in faq_data, f"Questions manquantes pour {category}"
            assert 'answer' in faq_data, f"Réponse manquante pour {category}"
            assert len(faq_data['questions']) > 0, f"Pas de questions pour {category}"
            assert len(faq_data['answer']) > 0, f"Réponse vide pour {category}"
            
            print(f"✅ FAQ {category}: {len(faq_data['questions'])} questions")
        
        # Test scénarios
        scenarios = ['mais_plantation', 'mais_recolte', 'pesticide_application']
        
        for scenario in scenarios:
            scenario_data = conversational_ai.scenarios[scenario]
            assert 'triggers' in scenario_data, f"Triggers manquants pour {scenario}"
            assert 'steps' in scenario_data, f"Steps manquants pour {scenario}"
            assert len(scenario_data['triggers']) > 0, f"Pas de triggers pour {scenario}"
            assert len(scenario_data['steps']) > 0, f"Pas d'étapes pour {scenario}"
            
            print(f"✅ Scénario {scenario}: {len(scenario_data['steps'])} étapes")
        
        # Test réponses par défaut
        default_responses = conversational_ai._get_default_response("message test")
        assert len(default_responses) > 0, "Réponse par défaut vide"
        
        print("✅ Réponses par défaut OK")
        
        print("🎉 FAQ et scénarios: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur FAQ et scénarios: {e}")
        return False

def test_intent_detection_accuracy():
    """Test de la précision de détection d'intention"""
    print("\n🎯 Test précision détection d'intention...")
    
    try:
        conversational_ai = ConversationalAI()
        
        # Test phrases complexes
        complex_messages = [
            ("Bonjour, je voudrais créer un business plan pour ma ferme", "business_plan"),
            ("Salut, pouvez-vous me dire la météo pour ma zone", "weather"),
            ("J'ai des feuilles jaunes sur mes plantes, c'est une maladie ?", "disease_diagnosis"),
            ("Combien coûte votre service premium ?", "payment"),
            ("Je ne sais pas comment utiliser votre application", "help"),
            ("Merci pour votre aide, au revoir", "goodbye")
        ]
        
        correct_detections = 0
        total_tests = len(complex_messages)
        
        for message, expected_intent in complex_messages:
            intent, confidence = conversational_ai._detect_intent(message)
            
            if intent == expected_intent:
                correct_detections += 1
                print(f"✅ '{message[:30]}...' -> {intent} ({confidence:.1%})")
            else:
                print(f"❌ '{message[:30]}...' -> {intent} (attendu: {expected_intent})")
        
        accuracy = correct_detections / total_tests
        print(f"📊 Précision: {correct_detections}/{total_tests} ({accuracy:.1%})")
        
        assert accuracy >= 0.7, f"Précision trop faible: {accuracy:.1%}"
        
        print("🎉 Précision de détection: Test réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test précision: {e}")
        return False

def run_week5_tests():
    """Exécute tous les tests de la semaine 5"""
    print("🚀 Début des tests Semaine 5 - Intelligence conversationnelle...\n")
    
    tests = [
        test_conversational_ai_service,
        test_message_processing,
        test_context_management,
        test_faq_and_scenarios,
        test_intent_detection_accuracy
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Résultats des tests Semaine 5:")
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passent! Services Semaine 5 prêts pour la production.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == '__main__':
    success = run_week5_tests()
    sys.exit(0 if success else 1) 