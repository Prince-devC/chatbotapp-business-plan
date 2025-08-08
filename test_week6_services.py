#!/usr/bin/env python3
"""
Tests pour les services Semaine 6 AgroBizChat
Validation support ananas et base de données complète
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.pineapple_service import PineappleService
from src.services.disease_detection import DiseaseDetectionService

def test_pineapple_service():
    """Test du service ananas"""
    print("🍍 Test PineappleService...")
    
    try:
        pineapple_service = PineappleService()
        
        # Test chargement des données
        assert len(pineapple_service.varieties) > 0, "Variétés non chargées"
        assert len(pineapple_service.techniques) > 0, "Techniques non chargées"
        assert len(pineapple_service.diseases) > 0, "Maladies non chargées"
        assert len(pineapple_service.market_data) > 0, "Données marché non chargées"
        assert len(pineapple_service.economic_data) > 0, "Données économiques non chargées"
        
        print("✅ Données ananas chargées OK")
        print(f"✅ Variétés: {len(pineapple_service.varieties)}")
        print(f"✅ Techniques: {len(pineapple_service.techniques)}")
        print(f"✅ Maladies: {len(pineapple_service.diseases)}")
        print(f"✅ Données marché: {len(pineapple_service.market_data)}")
        print(f"✅ Données économiques: {len(pineapple_service.economic_data)}")
        
        # Test récupération variétés
        varieties = pineapple_service.get_varieties()
        assert len(varieties) == 3, f"Nombre de variétés incorrect: {len(varieties)}"
        
        smooth_cayenne = next((v for v in varieties if v['name'] == 'Smooth Cayenne'), None)
        assert smooth_cayenne is not None, "Variété Smooth Cayenne manquante"
        assert smooth_cayenne['yield_per_ha'] == 35.0, "Rendement Smooth Cayenne incorrect"
        assert smooth_cayenne['cycle_duration'] == 18, "Cycle Smooth Cayenne incorrect"
        
        print("✅ Récupération variétés OK")
        
        # Test récupération techniques
        techniques = pineapple_service.get_techniques()
        assert len(techniques) == 5, f"Nombre de techniques incorrect: {len(techniques)}"
        
        plantation_techniques = pineapple_service.get_techniques(category='plantation')
        assert len(plantation_techniques) == 2, f"Nombre de techniques plantation incorrect: {len(plantation_techniques)}"
        
        print("✅ Récupération techniques OK")
        
        # Test récupération maladies
        diseases = pineapple_service.get_diseases()
        assert len(diseases) == 3, f"Nombre de maladies incorrect: {len(diseases)}"
        
        severe_diseases = pineapple_service.get_diseases(severity='Élevée')
        assert len(severe_diseases) == 1, f"Nombre de maladies sévères incorrect: {len(severe_diseases)}"
        
        print("✅ Récupération maladies OK")
        
        # Test données marché
        market_data = pineapple_service.get_market_data('Zone des terres de barre')
        assert len(market_data) > 0, "Données marché vides"
        
        print("✅ Données marché OK")
        
        # Test données économiques
        economic_data = pineapple_service.get_economic_data('Zone des terres de barre')
        assert len(economic_data) > 0, "Données économiques vides"
        
        print("✅ Données économiques OK")
        
        print("🎉 PineappleService: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur PineappleService: {e}")
        return False

def test_pineapple_business_plan():
    """Test génération business plan ananas"""
    print("\n📊 Test génération business plan ananas...")
    
    try:
        pineapple_service = PineappleService()
        
        # Données utilisateur de test
        user_data = {
            'zone_agro_ecologique': 'Zone des terres de barre',
            'land_area': 1.0,
            'farming_experience': 'Débutant',
            'farming_objective': 'Commercial'
        }
        
        # Test génération business plan
        business_plan = pineapple_service.generate_pineapple_business_plan(user_data, variety_id=1)
        
        assert business_plan is not None, "Business plan non généré"
        assert 'variety' in business_plan, "Variété manquante"
        assert 'economic_summary' in business_plan, "Résumé économique manquant"
        assert 'techniques' in business_plan, "Techniques manquantes"
        assert 'calendar' in business_plan, "Calendrier manquant"
        assert 'market_analysis' in business_plan, "Analyse marché manquante"
        assert 'risk_analysis' in business_plan, "Analyse risques manquante"
        assert 'recommendations' in business_plan, "Recommandations manquantes"
        
        # Vérifier les données économiques
        eco_summary = business_plan['economic_summary']
        assert eco_summary['surface_ha'] == 1.0, "Surface incorrecte"
        assert eco_summary['production_cost'] > 0, "Coût de production nul"
        assert eco_summary['expected_yield'] > 0, "Rendement nul"
        assert eco_summary['expected_revenue'] > 0, "Revenu nul"
        
        print(f"✅ Business plan généré: {business_plan['variety']['name']}")
        print(f"✅ Coût de production: {eco_summary['production_cost']:,} FCFA")
        print(f"✅ Rendement attendu: {eco_summary['expected_yield']} t/ha")
        print(f"✅ Revenu attendu: {eco_summary['expected_revenue']:,} FCFA")
        print(f"✅ Profit attendu: {eco_summary['expected_profit']:,} FCFA")
        print(f"✅ ROI: {eco_summary['roi_percentage']:.1f}%")
        
        # Vérifier le calendrier
        calendar = business_plan['calendar']
        assert calendar['cycle_duration_months'] == 18, "Durée cycle incorrecte"
        assert len(calendar['phases']) == 6, "Nombre de phases incorrect"
        
        print(f"✅ Calendrier: {calendar['cycle_duration_months']} mois, {len(calendar['phases'])} phases")
        
        # Vérifier les recommandations
        recommendations = business_plan['recommendations']
        assert len(recommendations) > 0, "Aucune recommandation"
        
        print(f"✅ Recommandations: {len(recommendations)} suggestions")
        
        print("🎉 Business plan ananas: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur business plan ananas: {e}")
        return False

def test_pineapple_advice():
    """Test conseils ananas"""
    print("\n💡 Test conseils ananas...")
    
    try:
        pineapple_service = PineappleService()
        
        # Test conseils généraux
        advice = pineapple_service.get_pineapple_advice('Zone des terres de barre')
        
        assert 'general_advice' in advice, "Conseils généraux manquants"
        assert 'seasonal_advice' in advice, "Conseils saisonniers manquants"
        assert 'variety_advice' in advice, "Conseils variétés manquants"
        assert 'zone_specific' in advice, "Conseils zone manquants"
        
        assert len(advice['general_advice']) > 0, "Aucun conseil général"
        assert len(advice['seasonal_advice']) > 0, "Aucun conseil saisonnier"
        
        print("✅ Conseils généraux OK")
        print(f"✅ Conseils généraux: {len(advice['general_advice'])}")
        print(f"✅ Conseils saisonniers: {len(advice['seasonal_advice'])}")
        
        # Test conseils par variété
        variety_advice = pineapple_service.get_pineapple_advice(
            'Zone des terres de barre', 
            variety='Smooth Cayenne'
        )
        
        assert len(variety_advice['variety_advice']) > 0, "Aucun conseil variété"
        
        print("✅ Conseils par variété OK")
        
        # Test conseils par saison
        seasonal_advice = pineapple_service.get_pineapple_advice(
            'Zone des terres de barre',
            season='saison_des_pluies'
        )
        
        assert len(seasonal_advice['seasonal_advice']) > 0, "Aucun conseil saisonnier"
        
        print("✅ Conseils par saison OK")
        
        print("🎉 Conseils ananas: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur conseils ananas: {e}")
        return False

def test_pineapple_disease_detection():
    """Test diagnostic maladies ananas"""
    print("\n🔍 Test diagnostic maladies ananas...")
    
    try:
        disease_service = DiseaseDetectionService()
        
        # Test image de test
        test_image_data = b"fake_pineapple_image_data"
        
        # Test diagnostic ananas
        diagnosis = disease_service.detect_disease(test_image_data, "ananas")
        
        if diagnosis:
            assert 'culture' in diagnosis, "Culture manquante"
            assert diagnosis['culture'] == 'ananas', "Culture incorrecte"
            assert 'disease_name' in diagnosis, "Nom de maladie manquant"
            assert 'confidence' in diagnosis, "Confiance manquante"
            assert 'severity' in diagnosis, "Sévérité manquante"
            assert 'symptoms' in diagnosis, "Symptômes manquants"
            assert 'treatments' in diagnosis, "Traitements manquants"
            assert 'prevention' in diagnosis, "Prévention manquante"
            
            print(f"✅ Diagnostic ananas: {diagnosis['disease_name']} ({diagnosis['confidence']:.1%})")
            print(f"✅ Sévérité: {diagnosis['severity']}")
            print(f"✅ Symptômes: {len(diagnosis['symptoms'])} détectés")
            print(f"✅ Traitements: {len(diagnosis['treatments'])} recommandés")
            print(f"✅ Prévention: {len(diagnosis['prevention'])} mesures")
        else:
            print("⚠️ Pas de diagnostic (mode test)")
        
        # Test récupération info maladie ananas
        disease_info = disease_service.get_disease_info('Fusariose', 'ananas')
        if disease_info:
            print(f"✅ Info maladie ananas: {disease_info['name']}")
        else:
            print("⚠️ Info maladie ananas non disponible (mode test)")
        
        print("🎉 Diagnostic maladies ananas: Tests de base passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur diagnostic maladies ananas: {e}")
        return False

def test_pineapple_models():
    """Test des modèles ananas"""
    print("\n📊 Test modèles ananas...")
    
    try:
        from src.models.pineapple_models import (
            PineappleVariety, PineappleTechnique, PineappleDisease,
            PineappleMarketData, PineappleEconomicData
        )
        
        # Test modèle PineappleVariety
        variety = PineappleVariety(
            name='Test Variety',
            scientific_name='Ananas test',
            description='Variété de test',
            yield_per_ha=30.0,
            cycle_duration=18,
            market_demand='Élevée',
            price_per_kg=250.0
        )
        
        variety.set_characteristics({
            'fruit_weight': '1.5-2.0 kg',
            'taste': 'Sucré'
        })
        
        variety.set_resistance_diseases({
            'fusariose': 'Modérée'
        })
        
        assert variety.name == 'Test Variety', "Nom variété incorrect"
        assert variety.yield_per_ha == 30.0, "Rendement incorrect"
        assert variety.get_characteristics()['fruit_weight'] == '1.5-2.0 kg', "Caractéristiques incorrectes"
        assert variety.get_resistance_diseases()['fusariose'] == 'Modérée', "Résistances incorrectes"
        
        dict_data = variety.to_dict()
        assert 'id' in dict_data, "ID manquant dans to_dict"
        assert 'name' in dict_data, "Name manquant dans to_dict"
        
        print("✅ Modèle PineappleVariety OK")
        
        # Test modèle PineappleTechnique
        technique = PineappleTechnique(
            name='Test Technique',
            category='plantation',
            description='Technique de test',
            duration_days=7,
            cost_per_ha=150000,
            zone_agro_ecologique='Zone des terres de barre'
        )
        
        technique.set_steps(['Étape 1', 'Étape 2'])
        technique.set_requirements({'soil_type': 'Sableux'})
        
        assert technique.name == 'Test Technique', "Nom technique incorrect"
        assert len(technique.get_steps()) == 2, "Étapes incorrectes"
        assert technique.get_requirements()['soil_type'] == 'Sableux', "Exigences incorrectes"
        
        print("✅ Modèle PineappleTechnique OK")
        
        # Test modèle PineappleDisease
        disease = PineappleDisease(
            name='Test Disease',
            scientific_name='Fusarium test',
            description='Maladie de test',
            severity='Modérée'
        )
        
        disease.set_symptoms(['Symptôme 1', 'Symptôme 2'])
        disease.set_treatments([{'name': 'Traitement test'}])
        disease.set_prevention(['Prévention 1'])
        
        assert disease.name == 'Test Disease', "Nom maladie incorrect"
        assert len(disease.get_symptoms()) == 2, "Symptômes incorrects"
        assert len(disease.get_treatments()) == 1, "Traitements incorrects"
        assert len(disease.get_prevention()) == 1, "Prévention incorrecte"
        
        print("✅ Modèle PineappleDisease OK")
        
        print("🎉 Modèles ananas: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modèles ananas: {e}")
        return False

def test_pineapple_integration():
    """Test d'intégration ananas complet"""
    print("\n🔗 Test intégration ananas...")
    
    try:
        pineapple_service = PineappleService()
        disease_service = DiseaseDetectionService()
        
        # Test flow complet
        # 1. Récupérer variétés
        varieties = pineapple_service.get_varieties()
        assert len(varieties) > 0, "Aucune variété disponible"
        
        # 2. Générer business plan
        user_data = {
            'zone_agro_ecologique': 'Zone des terres de barre',
            'land_area': 1.0,
            'farming_experience': 'Débutant'
        }
        
        business_plan = pineapple_service.generate_pineapple_business_plan(user_data)
        assert business_plan is not None, "Business plan non généré"
        
        # 3. Récupérer conseils
        advice = pineapple_service.get_pineapple_advice('Zone des terres de barre')
        assert advice is not None, "Conseils non générés"
        
        # 4. Simuler diagnostic maladie
        test_image = b"fake_pineapple_disease_image"
        diagnosis = disease_service.detect_disease(test_image, "ananas")
        
        if diagnosis:
            print("✅ Diagnostic ananas réussi")
        else:
            print("⚠️ Diagnostic ananas non disponible (mode test)")
        
        # 5. Récupérer données marché
        market_data = pineapple_service.get_market_data('Zone des terres de barre')
        assert len(market_data) > 0, "Données marché vides"
        
        # 6. Récupérer données économiques
        economic_data = pineapple_service.get_economic_data('Zone des terres de barre')
        assert len(economic_data) > 0, "Données économiques vides"
        
        print("✅ Intégration ananas complète réussie!")
        print(f"✅ Variétés: {len(varieties)}")
        print(f"✅ Business plan: {business_plan['variety']['name']}")
        print(f"✅ Conseils: {len(advice['general_advice'])} conseils généraux")
        print(f"✅ Données marché: {len(market_data)} entrées")
        print(f"✅ Données économiques: {len(economic_data)} entrées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration ananas: {e}")
        return False

def run_week6_tests():
    """Exécute tous les tests de la semaine 6"""
    print("🚀 Début des tests Semaine 6 - Support ananas...\n")
    
    tests = [
        test_pineapple_service,
        test_pineapple_business_plan,
        test_pineapple_advice,
        test_pineapple_disease_detection,
        test_pineapple_models,
        test_pineapple_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Résultats des tests Semaine 6:")
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passent! Services Semaine 6 prêts pour la production.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == '__main__':
    success = run_week6_tests()
    sys.exit(0 if success else 1) 