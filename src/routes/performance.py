"""
Routes pour les services de performance et monitoring
Cache, monitoring et optimisation base de données
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.cache_service import CacheService
from src.services.monitoring_service import MonitoringService
from src.services.database_optimizer import DatabaseOptimizer
import time

performance_bp = Blueprint('performance', __name__)

# Initialiser les services
cache_service = CacheService()
monitoring_service = MonitoringService()
db_optimizer = DatabaseOptimizer()

@performance_bp.route('/cache/health', methods=['GET'])
def cache_health():
    """
    Vérification de santé du cache
    """
    try:
        health = cache_service.health_check()
        return jsonify(health)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erreur vérification cache: {str(e)}'
        }), 500

@performance_bp.route('/cache/stats', methods=['GET'])
def cache_stats():
    """
    Statistiques du cache
    """
    try:
        stats = cache_service.get_cache_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur statistiques cache: {str(e)}'
        }), 500

@performance_bp.route('/cache/clear', methods=['POST'])
@jwt_required()
def clear_cache():
    """
    Efface le cache
    """
    try:
        data = request.get_json() or {}
        pattern = data.get('pattern', 'agrobiz:*')
        
        deleted_count = cache_service.clear_pattern(pattern)
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'pattern': pattern
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur effacement cache: {str(e)}'
        }), 500

@performance_bp.route('/cache/clear-user', methods=['POST'])
@jwt_required()
def clear_user_cache():
    """
    Efface le cache d'un utilisateur
    """
    try:
        user_id = get_jwt_identity()
        
        success = cache_service.clear_user_cache(str(user_id))
        
        return jsonify({
            'success': success,
            'user_id': user_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur effacement cache utilisateur: {str(e)}'
        }), 500

@performance_bp.route('/monitoring/metrics', methods=['GET'])
def get_metrics():
    """
    Récupère les métriques actuelles
    """
    try:
        metrics = monitoring_service.get_current_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur récupération métriques: {str(e)}'
        }), 500

@performance_bp.route('/monitoring/health', methods=['GET'])
def monitoring_health():
    """
    Vérification de santé du monitoring
    """
    try:
        health = monitoring_service.get_health_status()
        return jsonify(health)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erreur vérification monitoring: {str(e)}'
        }), 500

@performance_bp.route('/monitoring/api-stats', methods=['GET'])
def get_api_stats():
    """
    Statistiques des appels API
    """
    try:
        stats = monitoring_service.get_api_statistics()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur statistiques API: {str(e)}'
        }), 500

@performance_bp.route('/monitoring/error-stats', methods=['GET'])
def get_error_stats():
    """
    Statistiques des erreurs
    """
    try:
        stats = monitoring_service.get_error_statistics()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur statistiques erreurs: {str(e)}'
        }), 500

@performance_bp.route('/monitoring/summary', methods=['GET'])
def get_summary():
    """
    Rapport de synthèse
    """
    try:
        summary = monitoring_service.get_summary_report()
        return jsonify(summary)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur rapport synthèse: {str(e)}'
        }), 500

@performance_bp.route('/monitoring/export', methods=['GET'])
def export_metrics():
    """
    Export des métriques
    """
    try:
        format_type = request.args.get('format', 'json')
        metrics = monitoring_service.export_metrics(format_type)
        
        return jsonify({
            'success': True,
            'format': format_type,
            'data': metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur export métriques: {str(e)}'
        }), 500

@performance_bp.route('/database/optimize', methods=['POST'])
@jwt_required()
def optimize_database():
    """
    Optimise la base de données
    """
    try:
        result = db_optimizer.optimize_database()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erreur optimisation DB: {str(e)}'
        }), 500

@performance_bp.route('/database/create-indexes', methods=['POST'])
@jwt_required()
def create_indexes():
    """
    Crée les index de la base de données
    """
    try:
        result = db_optimizer.create_indexes()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erreur création index: {str(e)}'
        }), 500

@performance_bp.route('/database/stats', methods=['GET'])
def get_database_stats():
    """
    Statistiques de la base de données
    """
    try:
        stats = db_optimizer.get_database_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur statistiques DB: {str(e)}'
        }), 500

@performance_bp.route('/database/health', methods=['GET'])
def database_health():
    """
    Vérification de santé de la base de données
    """
    try:
        health = db_optimizer.health_check()
        return jsonify(health)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erreur vérification DB: {str(e)}'
        }), 500

@performance_bp.route('/database/analyze-query', methods=['POST'])
@jwt_required()
def analyze_query():
    """
    Analyse la performance d'une requête
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Requête manquante'
            }), 400
        
        result = db_optimizer.analyze_query_performance(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erreur analyse requête: {str(e)}'
        }), 500

@performance_bp.route('/database/suggestions', methods=['GET'])
def get_query_suggestions():
    """
    Suggestions d'optimisation
    """
    try:
        suggestions = db_optimizer.get_query_suggestions()
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erreur suggestions: {str(e)}'
        }), 500

@performance_bp.route('/performance/overview', methods=['GET'])
def performance_overview():
    """
    Vue d'ensemble des performances
    """
    try:
        # Récupérer toutes les métriques
        cache_health = cache_service.health_check()
        monitoring_health = monitoring_service.get_health_status()
        db_health = db_optimizer.health_check()
        cache_stats = cache_service.get_cache_stats()
        monitoring_summary = monitoring_service.get_summary_report()
        db_stats = db_optimizer.get_database_stats()
        
        overview = {
            'cache': {
                'health': cache_health,
                'stats': cache_stats
            },
            'monitoring': {
                'health': monitoring_health,
                'summary': monitoring_summary
            },
            'database': {
                'health': db_health,
                'stats': db_stats
            },
            'timestamp': time.time()
        }
        
        return jsonify({
            'success': True,
            'overview': overview
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur vue d\'ensemble: {str(e)}'
        }), 500

# Middleware pour mesurer les temps de réponse
@performance_bp.before_request
def before_request():
    """Mesure le temps de début de requête"""
    request.start_time = time.time()

@performance_bp.after_request
def after_request(response):
    """Mesure le temps de réponse et enregistre les métriques"""
    if hasattr(request, 'start_time'):
        response_time = time.time() - request.start_time
        
        # Enregistrer l'appel API
        endpoint = request.endpoint
        method = request.method
        status_code = response.status_code
        
        monitoring_service.log_api_call(endpoint, method, status_code, response_time)
    
    return response 