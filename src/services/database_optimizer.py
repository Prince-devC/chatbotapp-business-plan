"""
Service d'optimisation de base de données pour AgroBizChat
Index, requêtes optimisées et maintenance
"""

import sqlite3
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os

class DatabaseOptimizer:
    """Service d'optimisation de base de données"""
    
    def __init__(self, db_path: str = None):
        """
        Initialise l'optimiseur de base de données
        
        Args:
            db_path (str): Chemin vers la base de données
        """
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'app.db')
        self.optimization_enabled = os.getenv('DB_OPTIMIZATION_ENABLED', 'true').lower() == 'true'
    
    def create_indexes(self) -> Dict:
        """
        Crée les index pour optimiser les requêtes
        
        Returns:
            dict: Résultats de la création des index
        """
        if not self.optimization_enabled:
            return {'status': 'disabled', 'message': 'Optimisation désactivée'}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            indexes_created = []
            indexes_existing = []
            
            # Index pour la table users
            user_indexes = [
                ('idx_users_email', 'users', 'email'),
                ('idx_users_phone', 'users', 'phone'),
                ('idx_users_zone', 'users', 'zone_agro_ecologique'),
                ('idx_users_created_at', 'users', 'created_at')
            ]
            
            # Index pour la table conversations
            conversation_indexes = [
                ('idx_conversations_user_id', 'conversations', 'user_id'),
                ('idx_conversations_platform', 'conversations', 'platform'),
                ('idx_conversations_created_at', 'conversations', 'created_at')
            ]
            
            # Index pour la table messages
            message_indexes = [
                ('idx_messages_conversation_id', 'messages', 'conversation_id'),
                ('idx_messages_created_at', 'messages', 'created_at'),
                ('idx_messages_sender_type', 'messages', 'sender_type')
            ]
            
            # Index pour la table business_plans
            business_plan_indexes = [
                ('idx_business_plans_user_id', 'business_plans', 'user_id'),
                ('idx_business_plans_created_at', 'business_plans', 'created_at'),
                ('idx_business_plans_status', 'business_plans', 'status')
            ]
            
            # Index pour les tables ananas
            pineapple_indexes = [
                ('idx_pineapple_varieties_name', 'pineapple_varieties', 'name'),
                ('idx_pineapple_varieties_active', 'pineapple_varieties', 'is_active'),
                ('idx_pineapple_techniques_category', 'pineapple_techniques', 'category'),
                ('idx_pineapple_techniques_zone', 'pineapple_techniques', 'zone_agro_ecologique'),
                ('idx_pineapple_diseases_severity', 'pineapple_diseases', 'severity'),
                ('idx_pineapple_market_data_zone', 'pineapple_market_data', 'zone'),
                ('idx_pineapple_market_data_variety', 'pineapple_market_data', 'variety_id'),
                ('idx_pineapple_market_data_month_year', 'pineapple_market_data', 'month, year'),
                ('idx_pineapple_economic_data_zone', 'pineapple_economic_data', 'zone'),
                ('idx_pineapple_economic_data_variety', 'pineapple_economic_data', 'variety_id')
            ]
            
            # Index pour les tables de paiement
            payment_indexes = [
                ('idx_payment_transactions_user_id', 'payment_transactions', 'user_id'),
                ('idx_payment_transactions_status', 'payment_transactions', 'status'),
                ('idx_payment_transactions_created_at', 'payment_transactions', 'created_at'),
                ('idx_subscriptions_user_id', 'subscriptions', 'user_id'),
                ('idx_subscriptions_status', 'subscriptions', 'status'),
                ('idx_subscriptions_expires_at', 'subscriptions', 'expires_at')
            ]
            
            # Index pour les logs de diagnostic
            diagnosis_indexes = [
                ('idx_diagnosis_logs_user_id', 'diagnosis_logs', 'user_id'),
                ('idx_diagnosis_logs_culture', 'diagnosis_logs', 'culture'),
                ('idx_diagnosis_logs_created_at', 'diagnosis_logs', 'created_at')
            ]
            
            all_indexes = (
                user_indexes + conversation_indexes + message_indexes + 
                business_plan_indexes + pineapple_indexes + payment_indexes + diagnosis_indexes
            )
            
            for index_name, table_name, columns in all_indexes:
                try:
                    # Vérifier si l'index existe déjà
                    cursor.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='index' AND name=?
                    """, (index_name,))
                    
                    if cursor.fetchone():
                        indexes_existing.append(index_name)
                    else:
                        # Créer l'index
                        cursor.execute(f"""
                            CREATE INDEX {index_name} ON {table_name} ({columns})
                        """)
                        indexes_created.append(index_name)
                        
                except Exception as e:
                    print(f"Erreur création index {index_name}: {e}")
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'indexes_created': indexes_created,
                'indexes_existing': indexes_existing,
                'total_indexes': len(indexes_created) + len(indexes_existing)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur création index: {str(e)}'
            }
    
    def analyze_query_performance(self, query: str) -> Dict:
        """
        Analyse la performance d'une requête
        
        Args:
            query (str): Requête SQL à analyser
            
        Returns:
            dict: Analyse de performance
        """
        if not self.optimization_enabled:
            return {'status': 'disabled', 'message': 'Optimisation désactivée'}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Activer l'analyse des requêtes
            cursor.execute("PRAGMA analyze")
            
            # Exécuter EXPLAIN QUERY PLAN
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            query_plan = cursor.fetchall()
            
            # Obtenir des statistiques sur la requête
            cursor.execute("PRAGMA stats")
            stats = cursor.fetchall()
            
            conn.close()
            
            return {
                'status': 'success',
                'query': query,
                'query_plan': query_plan,
                'stats': stats
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur analyse requête: {str(e)}'
            }
    
    def optimize_database(self) -> Dict:
        """
        Optimise la base de données
        
        Returns:
            dict: Résultats de l'optimisation
        """
        if not self.optimization_enabled:
            return {'status': 'disabled', 'message': 'Optimisation désactivée'}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            optimizations = []
            
            # VACUUM pour réorganiser la base de données
            cursor.execute("VACUUM")
            optimizations.append("VACUUM - Réorganisation de la base de données")
            
            # ANALYZE pour mettre à jour les statistiques
            cursor.execute("ANALYZE")
            optimizations.append("ANALYZE - Mise à jour des statistiques")
            
            # Optimiser les paramètres SQLite
            cursor.execute("PRAGMA optimize")
            optimizations.append("PRAGMA optimize - Optimisation automatique")
            
            # Vérifier l'intégrité
            cursor.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()
            
            if integrity_result and integrity_result[0] == 'ok':
                optimizations.append("Intégrité de la base de données vérifiée")
            else:
                optimizations.append("⚠️ Problèmes d'intégrité détectés")
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'optimizations': optimizations,
                'integrity_ok': integrity_result and integrity_result[0] == 'ok'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur optimisation: {str(e)}'
            }
    
    def get_database_stats(self) -> Dict:
        """
        Récupère les statistiques de la base de données
        
        Returns:
            dict: Statistiques de la base de données
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Taille de la base de données
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            
            db_size_bytes = page_count * page_size
            db_size_mb = db_size_bytes / (1024 * 1024)
            
            # Nombre de tables
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            # Statistiques par table
            table_stats = {}
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_stats[table] = count
                except:
                    table_stats[table] = 0
            
            # Index existants
            cursor.execute("""
                SELECT name, tbl_name, sql FROM sqlite_master 
                WHERE type='index'
            """)
            indexes = cursor.fetchall()
            
            conn.close()
            
            return {
                'db_size_mb': round(db_size_mb, 2),
                'page_count': page_count,
                'page_size': page_size,
                'tables': tables,
                'table_stats': table_stats,
                'indexes_count': len(indexes),
                'indexes': [index[0] for index in indexes]
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur statistiques DB: {str(e)}'
            }
    
    def create_optimized_queries(self) -> Dict:
        """
        Crée des requêtes optimisées pour les opérations fréquentes
        
        Returns:
            dict: Requêtes optimisées créées
        """
        if not self.optimization_enabled:
            return {'status': 'disabled', 'message': 'Optimisation désactivée'}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Créer des vues optimisées
            views_created = []
            
            # Vue pour les utilisateurs actifs
            try:
                cursor.execute("""
                    CREATE VIEW IF NOT EXISTS active_users AS
                    SELECT id, email, phone, zone_agro_ecologique, farming_experience,
                           created_at, last_login_at
                    FROM users 
                    WHERE is_active = 1
                """)
                views_created.append("active_users")
            except Exception as e:
                print(f"Erreur création vue active_users: {e}")
            
            # Vue pour les business plans récents
            try:
                cursor.execute("""
                    CREATE VIEW IF NOT EXISTS recent_business_plans AS
                    SELECT bp.id, bp.user_id, u.email, bp.title, bp.status,
                           bp.created_at, bp.updated_at
                    FROM business_plans bp
                    JOIN users u ON bp.user_id = u.id
                    WHERE bp.created_at >= datetime('now', '-30 days')
                    ORDER BY bp.created_at DESC
                """)
                views_created.append("recent_business_plans")
            except Exception as e:
                print(f"Erreur création vue recent_business_plans: {e}")
            
            # Vue pour les diagnostics récents
            try:
                cursor.execute("""
                    CREATE VIEW IF NOT EXISTS recent_diagnoses AS
                    SELECT dl.id, dl.user_id, u.email, dl.culture, dl.disease_name,
                           dl.confidence, dl.created_at
                    FROM diagnosis_logs dl
                    JOIN users u ON dl.user_id = u.id
                    WHERE dl.created_at >= datetime('now', '-7 days')
                    ORDER BY dl.created_at DESC
                """)
                views_created.append("recent_diagnoses")
            except Exception as e:
                print(f"Erreur création vue recent_diagnoses: {e}")
            
            # Vue pour les paiements récents
            try:
                cursor.execute("""
                    CREATE VIEW IF NOT EXISTS recent_payments AS
                    SELECT pt.id, pt.user_id, u.email, pt.amount, pt.status,
                           pt.provider, pt.created_at
                    FROM payment_transactions pt
                    JOIN users u ON pt.user_id = u.id
                    WHERE pt.created_at >= datetime('now', '-30 days')
                    ORDER BY pt.created_at DESC
                """)
                views_created.append("recent_payments")
            except Exception as e:
                print(f"Erreur création vue recent_payments: {e}")
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'views_created': views_created,
                'total_views': len(views_created)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur création vues: {str(e)}'
            }
    
    def get_query_suggestions(self) -> Dict:
        """
        Suggère des optimisations de requêtes
        
        Returns:
            dict: Suggestions d'optimisation
        """
        suggestions = {
            'indexes': [
                "Créer des index sur les colonnes fréquemment utilisées dans WHERE",
                "Utiliser des index composites pour les requêtes multi-colonnes",
                "Indexer les colonnes de date pour les requêtes temporelles"
            ],
            'queries': [
                "Utiliser LIMIT pour limiter les résultats",
                "Éviter SELECT * et spécifier les colonnes nécessaires",
                "Utiliser des sous-requêtes au lieu de JOINs multiples",
                "Utiliser EXPLAIN QUERY PLAN pour analyser les performances"
            ],
            'maintenance': [
                "Exécuter VACUUM régulièrement pour réorganiser la base",
                "Utiliser ANALYZE pour mettre à jour les statistiques",
                "Surveiller la taille de la base de données",
                "Nettoyer les anciennes données non utilisées"
            ]
        }
        
        return {
            'status': 'success',
            'suggestions': suggestions
        }
    
    def health_check(self) -> Dict:
        """
        Vérification de santé de la base de données
        
        Returns:
            dict: État de santé de la base de données
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier l'intégrité
            cursor.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()
            
            # Vérifier la taille
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            
            db_size_mb = (page_count * page_size) / (1024 * 1024)
            
            # Vérifier les index
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
            index_count = cursor.fetchone()[0]
            
            # Vérifier les tables
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            
            conn.close()
            
            # Critères de santé
            integrity_ok = integrity_result and integrity_result[0] == 'ok'
            size_ok = db_size_mb < 100  # Moins de 100MB
            index_ok = index_count > 0  # Au moins un index
            
            if integrity_ok and size_ok and index_ok:
                status = 'healthy'
                message = 'Base de données en bonne santé'
            elif not integrity_ok:
                status = 'critical'
                message = 'Problèmes d\'intégrité détectés'
            elif not size_ok:
                status = 'warning'
                message = 'Base de données volumineuse'
            else:
                status = 'warning'
                message = 'Optimisations recommandées'
            
            return {
                'status': status,
                'message': message,
                'metrics': {
                    'integrity_ok': integrity_ok,
                    'size_mb': round(db_size_mb, 2),
                    'size_ok': size_ok,
                    'index_count': index_count,
                    'index_ok': index_ok,
                    'table_count': table_count
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur vérification santé: {str(e)}'
            } 