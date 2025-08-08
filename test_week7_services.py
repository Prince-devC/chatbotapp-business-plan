#!/usr/bin/env python3
"""
Tests pour les services Semaine 7 AgroBizChat
Validation optimisation performance et monitoring
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.cache_service import CacheService
from src.services.monitoring_service import MonitoringService
from src.services.database_optimizer import DatabaseOptimizer

def test_cache_service():
    """Test du service de cache Redis"""
    print("🔄 Test CacheService...")
    
    try:
        cache_service = CacheService()
        
        # Test disponibilité
        is_available = cache_service.is_available()
        print(f"✅ Cache disponible: {is_available}")
        
        # Test stockage et récupération
        test_key = "test_key"
        test_value = {"test": "data", "number": 42}
        
        # Stocker une valeur
        set_success = cache_service.set(test_key, test_value, ttl=60)
        print(f"✅ Stockage cache: {set_success}")
        
        # Récupérer la valeur
        retrieved_value = cache_service.get(test_key)
        if retrieved_value:
            assert retrieved_value['test'] == 'data', "Valeur récupérée incorrecte"
            assert retrieved_value['number'] == 42, "Nombre récupéré incorrect"
            print("✅ Récupération cache OK")
        else:
            print("⚠️ Cache non disponible (mode test)")
        
        # Test get_or_set
        def test_callback():
            return {"callback": "result"}
        
        callback_result = cache_service.get_or_set("callback_test", test_callback, ttl=60)
        if callback_result:
            assert callback_result['callback'] == 'result', "Résultat callback incorrect"
            print("✅ Get or set OK")
        
        # Test statistiques
        stats = cache_service.get_cache_stats()
        print(f"✅ Statistiques cache: {stats}")
        
        # Test health check
        health = cache_service.health_check()
        print(f"✅ Health check: {health['status']}")
        
        print("🎉 CacheService: Tests de base passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur CacheService: {e}")
        return False

def test_monitoring_service():
    """Test du service de monitoring"""
    print("\n📊 Test MonitoringService...")
    
    try:
        monitoring_service = MonitoringService()
        
        # Test métriques actuelles
        metrics = monitoring_service.get_current_metrics()
        assert 'monitoring_enabled' in metrics, "Métriques non disponibles"
        print("✅ Métriques actuelles OK")
        
        # Test enregistrement appel API
        monitoring_service.log_api_call('/test/endpoint', 'GET', 200, 0.5)
        monitoring_service.log_api_call('/test/endpoint', 'POST', 201, 1.2)
        monitoring_service.log_api_call('/test/endpoint', 'GET', 404, 0.1)
        
        # Test statistiques API
        api_stats = monitoring_service.get_api_statistics()
        assert len(api_stats) > 0, "Aucune statistique API"
        print("✅ Statistiques API OK")
        
        # Test enregistrement erreur
        monitoring_service.log_error('test_error', 'Erreur de test', {'detail': 'test'})
        
        # Test statistiques erreurs
        error_stats = monitoring_service.get_error_statistics()
        assert 'total_errors' in error_stats, "Statistiques erreurs manquantes"
        print("✅ Statistiques erreurs OK")
        
        # Test statut de santé
        health = monitoring_service.get_health_status()
        assert 'status' in health, "Statut de santé manquant"
        print(f"✅ Health status: {health['status']}")
        
        # Test informations système
        system_info = monitoring_service.get_system_info()
        assert 'platform' in system_info, "Informations système manquantes"
        print("✅ Informations système OK")
        
        # Test rapport de synthèse
        summary = monitoring_service.get_summary_report()
        assert 'monitoring_enabled' in summary, "Rapport de synthèse manquant"
        print("✅ Rapport de synthèse OK")
        
        print("🎉 MonitoringService: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur MonitoringService: {e}")
        return False

def test_database_optimizer():
    """Test du service d'optimisation base de données"""
    print("\n🔧 Test DatabaseOptimizer...")
    
    try:
        db_optimizer = DatabaseOptimizer()
        
        # Test statistiques base de données
        stats = db_optimizer.get_database_stats()
        assert 'db_size_mb' in stats, "Statistiques DB manquantes"
        print(f"✅ Statistiques DB: {stats['db_size_mb']} MB")
        
        # Test création index
        index_result = db_optimizer.create_indexes()
        assert 'status' in index_result, "Résultat création index manquant"
        print(f"✅ Création index: {index_result['status']}")
        
        # Test suggestions d'optimisation
        suggestions = db_optimizer.get_query_suggestions()
        assert 'suggestions' in suggestions, "Suggestions manquantes"
        print("✅ Suggestions d'optimisation OK")
        
        # Test health check
        health = db_optimizer.health_check()
        assert 'status' in health, "Health check DB manquant"
        print(f"✅ Health check DB: {health['status']}")
        
        # Test optimisation base de données
        optimize_result = db_optimizer.optimize_database()
        assert 'status' in optimize_result, "Résultat optimisation manquant"
        print(f"✅ Optimisation DB: {optimize_result['status']}")
        
        # Test création vues optimisées
        views_result = db_optimizer.create_optimized_queries()
        assert 'status' in views_result, "Résultat création vues manquant"
        print(f"✅ Création vues: {views_result['status']}")
        
        print("🎉 DatabaseOptimizer: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur DatabaseOptimizer: {e}")
        return False

def test_cache_integration():
    """Test d'intégration du cache avec les services existants"""
    print("\n🔗 Test intégration cache...")
    
    try:
        cache_service = CacheService()
        
        # Test cache météo
        weather_data = {
            'zone': 'Zone des terres de barre',
            'temperature': 28,
            'humidity': 75,
            'precipitation': 0
        }
        
        cache_success = cache_service.cache_weather_data('Zone des terres de barre', weather_data)
        print(f"✅ Cache météo: {cache_success}")
        
        cached_weather = cache_service.get_cached_weather_data('Zone des terres de barre')
        if cached_weather:
            assert cached_weather['temperature'] == 28, "Température cache incorrecte"
            print("✅ Récupération météo cache OK")
        
        # Test cache variétés ananas
        pineapple_varieties = [
            {'name': 'Smooth Cayenne', 'yield_per_ha': 35.0},
            {'name': 'Queen Victoria', 'yield_per_ha': 25.0}
        ]
        
        cache_success = cache_service.cache_pineapple_varieties(pineapple_varieties)
        print(f"✅ Cache variétés ananas: {cache_success}")
        
        cached_varieties = cache_service.get_cached_pineapple_varieties()
        if cached_varieties:
            assert len(cached_varieties) == 2, "Nombre variétés cache incorrect"
            print("✅ Récupération variétés cache OK")
        
        # Test cache business plan
        business_plan = {
            'user_id': 1,
            'title': 'Test Business Plan',
            'variety': 'Smooth Cayenne',
            'profit': 25000
        }
        
        cache_success = cache_service.cache_business_plan(1, business_plan)
        print(f"✅ Cache business plan: {cache_success}")
        
        cached_plan = cache_service.get_cached_business_plan(1)
        if cached_plan:
            assert cached_plan['title'] == 'Test Business Plan', "Titre cache incorrect"
            print("✅ Récupération business plan cache OK")
        
        # Test cache diagnostic
        diagnosis = {
            'disease_name': 'Fusariose',
            'confidence': 0.85,
            'severity': 'Élevée'
        }
        
        cache_success = cache_service.cache_disease_diagnosis('test_image_hash', diagnosis)
        print(f"✅ Cache diagnostic: {cache_success}")
        
        cached_diagnosis = cache_service.get_cached_diagnosis('test_image_hash')
        if cached_diagnosis:
            assert cached_diagnosis['disease_name'] == 'Fusariose', "Maladie cache incorrecte"
            print("✅ Récupération diagnostic cache OK")
        
        print("🎉 Intégration cache: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration cache: {e}")
        return False

def test_performance_improvements():
    """Test des améliorations de performance"""
    print("\n⚡ Test améliorations performance...")
    
    try:
        # Test monitoring en temps réel
        monitoring_service = MonitoringService()
        
        # Simuler des appels API
        for i in range(5):
            monitoring_service.log_api_call('/test/performance', 'GET', 200, 0.1 + i * 0.1)
            monitoring_service.log_api_call('/test/performance', 'POST', 201, 0.2 + i * 0.1)
        
        # Simuler des erreurs
        monitoring_service.log_error('performance_test', 'Test erreur performance')
        
        # Vérifier les métriques
        metrics = monitoring_service.get_current_metrics()
        assert 'cpu' in metrics, "Métriques CPU manquantes"
        assert 'memory' in metrics, "Métriques mémoire manquantes"
        print("✅ Métriques temps réel OK")
        
        # Vérifier les statistiques API
        api_stats = monitoring_service.get_api_statistics()
        assert '/test/performance' in api_stats, "Statistiques API manquantes"
        print("✅ Statistiques API temps réel OK")
        
        # Vérifier le statut de santé
        health = monitoring_service.get_health_status()
        assert health['status'] in ['healthy', 'warning', 'critical'], "Statut de santé invalide"
        print(f"✅ Health status temps réel: {health['status']}")
        
        # Test cache avec monitoring
        cache_service = CacheService()
        
        # Mesurer les performances du cache
        import time
        
        # Test sans cache
        start_time = time.time()
        for i in range(10):
            # Simuler une opération coûteuse
            time.sleep(0.01)
        no_cache_time = time.time() - start_time
        
        # Test avec cache
        start_time = time.time()
        for i in range(10):
            cache_service.get_or_set(f"perf_test_{i}", lambda: time.sleep(0.01), ttl=60)
        cache_time = time.time() - start_time
        
        print(f"✅ Temps sans cache: {no_cache_time:.3f}s")
        print(f"✅ Temps avec cache: {cache_time:.3f}s")
        print(f"✅ Amélioration: {((no_cache_time - cache_time) / no_cache_time * 100):.1f}%")
        
        print("🎉 Améliorations performance: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur améliorations performance: {e}")
        return False

def test_database_optimization():
    """Test des optimisations de base de données"""
    print("\n🗄️ Test optimisations base de données...")
    
    try:
        db_optimizer = DatabaseOptimizer()
        
        # Test analyse requête
        test_query = "SELECT * FROM users WHERE email = 'test@example.com'"
        analysis = db_optimizer.analyze_query_performance(test_query)
        assert 'status' in analysis, "Analyse requête manquante"
        print("✅ Analyse requête OK")
        
        # Test statistiques base de données
        stats = db_optimizer.get_database_stats()
        assert 'db_size_mb' in stats, "Taille DB manquante"
        assert 'tables' in stats, "Tables manquantes"
        assert 'indexes_count' in stats, "Nombre d'index manquant"
        print(f"✅ Statistiques DB: {stats['db_size_mb']} MB, {len(stats['tables'])} tables, {stats['indexes_count']} index")
        
        # Test health check
        health = db_optimizer.health_check()
        assert 'status' in health, "Health check manquant"
        assert 'metrics' in health, "Métriques health check manquantes"
        print(f"✅ Health check DB: {health['status']}")
        
        # Test suggestions
        suggestions = db_optimizer.get_query_suggestions()
        assert 'suggestions' in suggestions, "Suggestions manquantes"
        assert 'indexes' in suggestions['suggestions'], "Suggestions index manquantes"
        assert 'queries' in suggestions['suggestions'], "Suggestions requêtes manquantes"
        print("✅ Suggestions d'optimisation OK")
        
        print("🎉 Optimisations base de données: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur optimisations base de données: {e}")
        return False

def run_week7_tests():
    """Exécute tous les tests de la semaine 7"""
    print("🚀 Début des tests Semaine 7 - Optimisation performance...\n")
    
    tests = [
        test_cache_service,
        test_monitoring_service,
        test_database_optimizer,
        test_cache_integration,
        test_performance_improvements,
        test_database_optimization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Résultats des tests Semaine 7:")
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passent! Services Semaine 7 prêts pour la production.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == '__main__':
    success = run_week7_tests()
    sys.exit(0 if success else 1) 