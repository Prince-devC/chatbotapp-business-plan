"""
Service de monitoring pour AgroBizChat
Surveillance des performances et métriques
"""

import time
import psutil
import threading
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os

class MonitoringService:
    """Service de monitoring pour surveiller les performances"""
    
    def __init__(self):
        self.metrics = {}
        self.performance_data = []
        self.error_logs = []
        self.api_calls = {}
        self.start_time = datetime.now()
        self.monitoring_enabled = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
        
        if self.monitoring_enabled:
            self._start_background_monitoring()
    
    def _start_background_monitoring(self):
        """Démarre le monitoring en arrière-plan"""
        def monitor_loop():
            while True:
                try:
                    self._collect_system_metrics()
                    time.sleep(60)  # Collecte toutes les minutes
                except Exception as e:
                    print(f"Erreur monitoring: {e}")
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        print("✅ Monitoring démarré en arrière-plan")
    
    def _collect_system_metrics(self):
        """Collecte les métriques système"""
        try:
            # Métriques CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Métriques mémoire
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            
            # Métriques disque
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used = disk.used / (1024**3)  # GB
            disk_total = disk.total / (1024**3)  # GB
            
            # Métriques réseau
            network = psutil.net_io_counters()
            bytes_sent = network.bytes_sent
            bytes_recv = network.bytes_recv
            
            # Uptime
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'percent': memory_percent,
                    'used_gb': round(memory_used, 2),
                    'total_gb': round(memory_total, 2)
                },
                'disk': {
                    'percent': disk_percent,
                    'used_gb': round(disk_used, 2),
                    'total_gb': round(disk_total, 2)
                },
                'network': {
                    'bytes_sent': bytes_sent,
                    'bytes_recv': bytes_recv
                },
                'uptime_seconds': uptime
            }
            
            self.performance_data.append(metrics)
            
            # Garder seulement les 1000 dernières métriques
            if len(self.performance_data) > 1000:
                self.performance_data = self.performance_data[-1000:]
            
            self.metrics = metrics
            
        except Exception as e:
            print(f"Erreur collecte métriques: {e}")
    
    def log_api_call(self, endpoint: str, method: str, status_code: int, response_time: float):
        """
        Enregistre un appel API
        
        Args:
            endpoint (str): Endpoint appelé
            method (str): Méthode HTTP
            status_code (int): Code de statut
            response_time (float): Temps de réponse en secondes
        """
        if not self.monitoring_enabled:
            return
        
        call_data = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'response_time': response_time
        }
        
        # Enregistrer dans les métriques
        if endpoint not in self.api_calls:
            self.api_calls[endpoint] = []
        
        self.api_calls[endpoint].append(call_data)
        
        # Garder seulement les 100 derniers appels par endpoint
        if len(self.api_calls[endpoint]) > 100:
            self.api_calls[endpoint] = self.api_calls[endpoint][-100:]
    
    def log_error(self, error_type: str, message: str, details: Dict = None):
        """
        Enregistre une erreur
        
        Args:
            error_type (str): Type d'erreur
            message (str): Message d'erreur
            details (dict): Détails supplémentaires
        """
        if not self.monitoring_enabled:
            return
        
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': message,
            'details': details or {}
        }
        
        self.error_logs.append(error_data)
        
        # Garder seulement les 500 dernières erreurs
        if len(self.error_logs) > 500:
            self.error_logs = self.error_logs[-500:]
    
    def get_current_metrics(self) -> Dict:
        """
        Récupère les métriques actuelles
        
        Returns:
            dict: Métriques système actuelles
        """
        if not self.monitoring_enabled:
            return {
                'monitoring_enabled': False,
                'message': 'Monitoring désactivé'
            }
        
        return {
            'monitoring_enabled': True,
            'current_metrics': self.metrics,
            'uptime': (datetime.now() - self.start_time).total_seconds(),
            'start_time': self.start_time.isoformat()
        }
    
    def get_performance_history(self, hours: int = 24) -> List[Dict]:
        """
        Récupère l'historique des performances
        
        Args:
            hours (int): Nombre d'heures à récupérer
            
        Returns:
            list: Historique des performances
        """
        if not self.monitoring_enabled:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        return [
            metric for metric in self.performance_data
            if datetime.fromisoformat(metric['timestamp']) > cutoff_time
        ]
    
    def get_api_statistics(self) -> Dict:
        """
        Récupère les statistiques des appels API
        
        Returns:
            dict: Statistiques des API
        """
        if not self.monitoring_enabled:
            return {}
        
        stats = {}
        
        for endpoint, calls in self.api_calls.items():
            if not calls:
                continue
            
            # Calculer les statistiques
            response_times = [call['response_time'] for call in calls]
            status_codes = [call['status_code'] for call in calls]
            
            # Répartition des codes de statut
            status_distribution = {}
            for status in status_codes:
                status_distribution[status] = status_distribution.get(status, 0) + 1
            
            stats[endpoint] = {
                'total_calls': len(calls),
                'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
                'min_response_time': min(response_times) if response_times else 0,
                'max_response_time': max(response_times) if response_times else 0,
                'status_distribution': status_distribution,
                'last_call': calls[-1]['timestamp'] if calls else None
            }
        
        return stats
    
    def get_error_statistics(self) -> Dict:
        """
        Récupère les statistiques des erreurs
        
        Returns:
            dict: Statistiques des erreurs
        """
        if not self.monitoring_enabled:
            return {}
        
        if not self.error_logs:
            return {
                'total_errors': 0,
                'error_types': {},
                'recent_errors': []
            }
        
        # Répartition par type d'erreur
        error_types = {}
        for error in self.error_logs:
            error_type = error['type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'total_errors': len(self.error_logs),
            'error_types': error_types,
            'recent_errors': self.error_logs[-10:]  # 10 dernières erreurs
        }
    
    def get_health_status(self) -> Dict:
        """
        Récupère le statut de santé de l'application
        
        Returns:
            dict: Statut de santé
        """
        if not self.monitoring_enabled:
            return {
                'status': 'monitoring_disabled',
                'message': 'Monitoring désactivé'
            }
        
        try:
            # Vérifier les métriques système
            if not self.metrics:
                return {
                    'status': 'unknown',
                    'message': 'Aucune métrique disponible'
                }
            
            # Critères de santé
            cpu_ok = self.metrics.get('cpu', {}).get('percent', 0) < 90
            memory_ok = self.metrics.get('memory', {}).get('percent', 0) < 90
            disk_ok = self.metrics.get('disk', {}).get('percent', 0) < 90
            
            # Vérifier les erreurs récentes
            recent_errors = [
                error for error in self.error_logs
                if datetime.fromisoformat(error['timestamp']) > datetime.now() - timedelta(hours=1)
            ]
            
            errors_ok = len(recent_errors) < 10  # Moins de 10 erreurs par heure
            
            if cpu_ok and memory_ok and disk_ok and errors_ok:
                status = 'healthy'
                message = 'Application en bonne santé'
            elif not errors_ok:
                status = 'warning'
                message = 'Trop d\'erreurs récentes'
            else:
                status = 'critical'
                message = 'Ressources système critiques'
            
            return {
                'status': status,
                'message': message,
                'metrics': {
                    'cpu_ok': cpu_ok,
                    'memory_ok': memory_ok,
                    'disk_ok': disk_ok,
                    'errors_ok': errors_ok
                },
                'recent_errors_count': len(recent_errors)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur monitoring: {str(e)}'
            }
    
    def get_system_info(self) -> Dict:
        """
        Récupère les informations système
        
        Returns:
            dict: Informations système
        """
        try:
            return {
                'platform': psutil.sys.platform,
                'python_version': psutil.sys.version,
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'disk_total_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def export_metrics(self, format: str = 'json') -> str:
        """
        Exporte les métriques
        
        Args:
            format (str): Format d'export (json, csv)
            
        Returns:
            str: Métriques exportées
        """
        if not self.monitoring_enabled:
            return "Monitoring désactivé"
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'system_info': self.get_system_info(),
            'current_metrics': self.metrics,
            'api_statistics': self.get_api_statistics(),
            'error_statistics': self.get_error_statistics(),
            'performance_history': self.get_performance_history(24)
        }
        
        if format == 'json':
            return json.dumps(export_data, indent=2, ensure_ascii=False)
        else:
            return str(export_data)
    
    def clear_old_data(self, days: int = 7):
        """
        Efface les anciennes données
        
        Args:
            days (int): Nombre de jours à conserver
        """
        if not self.monitoring_enabled:
            return
        
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # Effacer les anciennes métriques de performance
        self.performance_data = [
            metric for metric in self.performance_data
            if datetime.fromisoformat(metric['timestamp']) > cutoff_time
        ]
        
        # Effacer les anciens appels API
        for endpoint in self.api_calls:
            self.api_calls[endpoint] = [
                call for call in self.api_calls[endpoint]
                if datetime.fromisoformat(call['timestamp']) > cutoff_time
            ]
        
        # Effacer les anciennes erreurs
        self.error_logs = [
            error for error in self.error_logs
            if datetime.fromisoformat(error['timestamp']) > cutoff_time
        ]
        
        print(f"✅ Données de monitoring nettoyées (conservées: {days} jours)")
    
    def get_summary_report(self) -> Dict:
        """
        Génère un rapport de synthèse
        
        Returns:
            dict: Rapport de synthèse
        """
        if not self.monitoring_enabled:
            return {
                'monitoring_enabled': False,
                'message': 'Monitoring désactivé'
            }
        
        try:
            # Statistiques générales
            uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
            total_api_calls = sum(len(calls) for calls in self.api_calls.values())
            total_errors = len(self.error_logs)
            
            # Métriques actuelles
            current_cpu = self.metrics.get('cpu', {}).get('percent', 0)
            current_memory = self.metrics.get('memory', {}).get('percent', 0)
            current_disk = self.metrics.get('disk', {}).get('percent', 0)
            
            # Endpoints les plus utilisés
            endpoint_usage = {}
            for endpoint, calls in self.api_calls.items():
                endpoint_usage[endpoint] = len(calls)
            
            top_endpoints = sorted(endpoint_usage.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                'monitoring_enabled': True,
                'uptime_hours': round(uptime_hours, 2),
                'total_api_calls': total_api_calls,
                'total_errors': total_errors,
                'current_metrics': {
                    'cpu_percent': current_cpu,
                    'memory_percent': current_memory,
                    'disk_percent': current_disk
                },
                'top_endpoints': top_endpoints,
                'health_status': self.get_health_status(),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'monitoring_enabled': True,
                'error': str(e),
                'message': 'Erreur lors de la génération du rapport'
            } 