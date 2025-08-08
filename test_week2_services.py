#!/usr/bin/env python3
"""
Tests pour les services Semaine 2 AgroBizChat
Validation météo et PDF enrichi
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.weather_service import WeatherService
from src.services.enhanced_pdf_generator import EnhancedPDFGenerator
from src.services.unit_converter import UnitConverter

def test_weather_service_enhanced():
    """Test du service météo amélioré"""
    print("🌦️ Test WeatherService amélioré...")
    
    try:
        weather_service = WeatherService(use_sandbox=True)
        
        # Test zones agro-écologiques
        zones = [
            "Zone côtière",
            "Zone des terres de barre", 
            "Zone des collines",
            "Zone de l'Atacora",
            "Zone de la Donga"
        ]
        
        for zone in zones:
            # Test météo actuelle
            weather = weather_service.get_current_weather(zone)
            assert weather is not None, f"Pas de données météo pour {zone}"
            assert 'temperature' in weather, f"Température manquante pour {zone}"
            assert 'humidity' in weather, f"Humidité manquante pour {zone}"
            assert 'zone' in weather, f"Zone manquante pour {zone}"
            print(f"✅ Météo {zone}: {weather['temperature']}°C, {weather['humidity']}%")
        
        # Test prévisions
        forecast = weather_service.get_forecast("Zone des terres de barre", 7)
        assert forecast is not None, "Pas de prévisions"
        assert len(forecast) == 7, f"Nombre de jours incorrect: {len(forecast)}"
        print(f"✅ Prévisions: {len(forecast)} jours")
        
        # Test conseils agro-météo
        advice = weather_service.get_agro_advice("Zone des terres de barre", "mais")
        assert advice is not None, "Pas de conseils agro-météo"
        assert 'culture' in advice, "Culture manquante dans les conseils"
        assert 'conseils' in advice, "Conseils manquants"
        assert 'actions_immediates' in advice, "Actions immédiates manquantes"
        assert 'planification' in advice, "Planification manquante"
        print(f"✅ Conseils agro-météo: {len(advice.get('conseils', []))} conseils")
        
        print("🎉 WeatherService amélioré: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur WeatherService amélioré: {e}")
        return False

def test_enhanced_pdf_generator():
    """Test du générateur PDF enrichi"""
    print("\n📄 Test EnhancedPDFGenerator...")
    
    try:
        pdf_generator = EnhancedPDFGenerator()
        
        # Données de test
        user_data = {
            'username': 'Agriculteur Test',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'user_type': 'individuel',
            'zone_agro_ecologique': 'Zone des terres de barre',
            'farming_objective': 'commercial',
            'land_area': 2.5,
            'land_unit': 'ha',
            'farming_experience': 'intermediaire',
            'primary_culture': 'mais'
        }
        
        weather_data = {
            'culture': 'mais',
            'conditions_actuelles': {
                'temperature': '28°C',
                'humidity': '75%',
                'precipitation': '5mm',
                'description': 'Ensoleillé avec quelques nuages',
                'zone': 'Zone des terres de barre'
            },
            'conseils': [
                'Température favorable pour la croissance du maïs',
                'Humidité adéquate, surveillance normale'
            ],
            'actions_immediates': [
                'Continuer les soins culturaux',
                'Surveiller les ravageurs'
            ],
            'planification': [
                'Préparer la récolte dans 2-3 semaines'
            ]
        }
        
        business_data = {
            'operating_costs': 150000,
            'fixed_costs': 50000,
            'expected_revenue': 300000,
            'gross_margin': 150000,
            'net_result': 100000
        }
        
        # Test génération PDF
        pdf_path = pdf_generator.generate_business_plan_pdf(
            user_data=user_data,
            weather_data=weather_data,
            business_data=business_data,
            output_path="test_business_plan_enhanced.pdf"
        )
        
        assert os.path.exists(pdf_path), f"PDF non généré: {pdf_path}"
        assert pdf_path.endswith('.pdf'), "Extension PDF incorrecte"
        
        file_size = os.path.getsize(pdf_path)
        assert file_size > 1000, f"PDF trop petit: {file_size} bytes"
        
        print(f"✅ PDF généré: {pdf_path} ({file_size} bytes)")
        
        # Test plans d'action
        current_month = 6  # Juin
        plan_30 = pdf_generator._get_mais_30_days_plan(current_month, weather_data)
        plan_60 = pdf_generator._get_mais_60_days_plan(current_month, weather_data)
        plan_90 = pdf_generator._get_mais_90_days_plan(current_month, weather_data)
        
        assert len(plan_30) > 0, "Plan 30 jours vide"
        assert len(plan_60) > 0, "Plan 60 jours vide"
        assert len(plan_90) > 0, "Plan 90 jours vide"
        
        print(f"✅ Plans d'action: 30j({len(plan_30)}), 60j({len(plan_60)}), 90j({len(plan_90)})")
        
        # Nettoyer le fichier de test
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print("✅ Fichier de test nettoyé")
        
        print("🎉 EnhancedPDFGenerator: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur EnhancedPDFGenerator: {e}")
        return False

def test_integration_weather_pdf():
    """Test d'intégration météo + PDF"""
    print("\n🔗 Test intégration météo + PDF...")
    
    try:
        weather_service = WeatherService(use_sandbox=True)
        pdf_generator = EnhancedPDFGenerator()
        
        # Récupérer des données météo réelles
        weather_data = weather_service.get_agro_advice("Zone des terres de barre", "mais")
        
        if weather_data:
            # Générer un PDF avec les vraies données météo
            user_data = {
                'username': 'Test Intégration',
                'first_name': 'Test',
                'last_name': 'Intégration',
                'user_type': 'individuel',
                'zone_agro_ecologique': 'Zone des terres de barre',
                'farming_objective': 'commercial',
                'land_area': 3.0,
                'land_unit': 'ha',
                'farming_experience': 'expert',
                'primary_culture': 'mais'
            }
            
            business_data = {
                'operating_costs': 200000,
                'fixed_costs': 75000,
                'expected_revenue': 450000,
                'gross_margin': 250000,
                'net_result': 175000
            }
            
            pdf_path = pdf_generator.generate_business_plan_pdf(
                user_data=user_data,
                weather_data=weather_data,
                business_data=business_data,
                output_path="test_integration_weather.pdf"
            )
            
            assert os.path.exists(pdf_path), "PDF d'intégration non généré"
            
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF d'intégration généré: {pdf_path} ({file_size} bytes)")
            
            # Nettoyer
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            
            print("✅ Intégration météo + PDF réussie!")
        else:
            print("⚠️ Pas de données météo pour l'intégration")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration: {e}")
        return False

def test_zone_mapping():
    """Test du mapping des zones agro-écologiques"""
    print("\n🗺️ Test mapping zones agro-écologiques...")
    
    try:
        weather_service = WeatherService()
        
        # Test toutes les zones
        zones = [
            "Zone côtière",
            "Zone des terres de barre",
            "Zone des collines", 
            "Zone de l'Atacora",
            "Zone de la Donga",
            "Zone de l'Ouémé",
            "Zone de l'Alibori",
            "Zone du Borgou",
            "Zone du Mono",
            "Zone du Couffo"
        ]
        
        for zone in zones:
            coords = weather_service._get_zone_coordinates(zone)
            assert coords is not None, f"Coordonnées manquantes pour {zone}"
            assert 'lat' in coords, f"Latitude manquante pour {zone}"
            assert 'lon' in coords, f"Longitude manquante pour {zone}"
            assert 'name' in coords, f"Nom manquant pour {zone}"
            print(f"✅ Zone {zone}: {coords['name']} ({coords['lat']}, {coords['lon']})")
        
        print("🎉 Mapping zones: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur mapping zones: {e}")
        return False

def run_week2_tests():
    """Exécute tous les tests de la semaine 2"""
    print("🚀 Début des tests Semaine 2 - API Météo & PDF enrichi...\n")
    
    tests = [
        test_weather_service_enhanced,
        test_enhanced_pdf_generator,
        test_integration_weather_pdf,
        test_zone_mapping
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Résultats des tests Semaine 2:")
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passent! Services Semaine 2 prêts pour la production.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == '__main__':
    success = run_week2_tests()
    sys.exit(0 if success else 1) 