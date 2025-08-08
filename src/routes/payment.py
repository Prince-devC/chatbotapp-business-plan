"""
Routes pour les paiements et modèle freemium
Intégration Kkiapay et PayDunya
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os
import json

from src.models.database import db, User
from src.models.payment_models import PaymentTransaction, Subscription
from src.services.payment_service import PaymentService
from src.services.enhanced_pdf_generator import EnhancedPDFGenerator

payment_bp = Blueprint('payment', __name__)

# Initialiser les services
payment_service = PaymentService(provider="kkiapay")  # Par défaut Kkiapay
pdf_generator = EnhancedPDFGenerator()

@payment_bp.route('/packages', methods=['GET'])
def get_pricing_packages():
    """
    Récupère les packages de prix disponibles
    """
    try:
        packages = payment_service.get_pricing_packages()
        
        return jsonify({
            'success': True,
            'packages': packages
        })
        
    except Exception as e:
        print(f"Erreur récupération packages: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des packages'}), 500

@payment_bp.route('/create-payment', methods=['POST'])
@jwt_required()
def create_payment():
    """
    Crée une transaction de paiement
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        package_id = data.get('package_id')
        provider = data.get('provider', 'kkiapay')
        
        # Récupérer l'utilisateur
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Récupérer les packages
        packages = payment_service.get_pricing_packages()
        selected_package = next((p for p in packages if p['id'] == package_id), None)
        
        if not selected_package:
            return jsonify({'error': 'Package non trouvé'}), 404
        
        # Créer le paiement
        payment_data = payment_service.create_payment(
            amount=selected_package['price'],
            user_id=str(user_id),
            description=f"Pack {selected_package['name']} - AgroBizChat",
            phone_number=user.phone_number,
            email=user.email
        )
        
        if payment_data:
            # Enregistrer la transaction en base
            transaction = PaymentTransaction(
                user_id=user_id,
                package_id=package_id,
                amount=selected_package['price'],
                currency='XOF',
                provider=provider,
                payment_id=payment_data['payment_id'],
                reference=payment_data['reference'],
                status='pending',
                payment_url=payment_data['payment_url']
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'payment_data': payment_data,
                'package': selected_package
            })
        else:
            return jsonify({'error': 'Erreur lors de la création du paiement'}), 500
        
    except Exception as e:
        print(f"Erreur création paiement: {e}")
        return jsonify({'error': 'Erreur lors de la création du paiement'}), 500

@payment_bp.route('/verify-payment/<payment_id>', methods=['GET'])
@jwt_required()
def verify_payment(payment_id):
    """
    Vérifie le statut d'un paiement
    """
    try:
        user_id = get_jwt_identity()
        
        # Vérifier le paiement
        payment_status = payment_service.verify_payment(payment_id)
        
        if payment_status:
            # Mettre à jour la transaction en base
            transaction = PaymentTransaction.query.filter_by(
                payment_id=payment_id,
                user_id=user_id
            ).first()
            
            if transaction:
                transaction.status = payment_status['status']
                transaction.paid_at = datetime.now() if payment_status['status'] == 'completed' else None
                db.session.commit()
                
                # Si paiement réussi, créer l'abonnement
                if payment_status['status'] == 'completed':
                    create_subscription(user_id, transaction.package_id)
                
                return jsonify({
                    'success': True,
                    'payment_status': payment_status,
                    'transaction': transaction.to_dict()
                })
            else:
                return jsonify({'error': 'Transaction non trouvée'}), 404
        else:
            return jsonify({'error': 'Erreur lors de la vérification'}), 500
        
    except Exception as e:
        print(f"Erreur vérification paiement: {e}")
        return jsonify({'error': 'Erreur lors de la vérification'}), 500

@payment_bp.route('/webhook/payment', methods=['POST'])
def payment_webhook():
    """
    Webhook pour les notifications de paiement
    """
    try:
        data = request.get_json()
        signature = request.headers.get('X-Signature')
        
        # Traiter le webhook
        webhook_data = payment_service.process_webhook(data, signature)
        
        if webhook_data:
            # Mettre à jour la transaction
            transaction = PaymentTransaction.query.filter_by(
                payment_id=webhook_data['payment_id']
            ).first()
            
            if transaction:
                transaction.status = webhook_data['status']
                transaction.paid_at = datetime.now() if webhook_data['status'] == 'completed' else None
                db.session.commit()
                
                # Si paiement réussi, créer l'abonnement
                if webhook_data['status'] == 'completed':
                    create_subscription(transaction.user_id, transaction.package_id)
                
                return jsonify({'success': True})
            else:
                print(f"Transaction non trouvée pour payment_id: {webhook_data['payment_id']}")
                return jsonify({'error': 'Transaction non trouvée'}), 404
        else:
            return jsonify({'error': 'Webhook invalide'}), 400
        
    except Exception as e:
        print(f"Erreur webhook paiement: {e}")
        return jsonify({'error': 'Erreur webhook'}), 500

@payment_bp.route('/subscription/status', methods=['GET'])
@jwt_required()
def get_subscription_status():
    """
    Récupère le statut de l'abonnement de l'utilisateur
    """
    try:
        user_id = get_jwt_identity()
        
        # Récupérer l'abonnement actif
        subscription = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if subscription:
            return jsonify({
                'success': True,
                'subscription': subscription.to_dict(),
                'features': get_package_features(subscription.package_id)
            })
        else:
            return jsonify({
                'success': True,
                'subscription': None,
                'features': get_package_features('free')
            })
        
    except Exception as e:
        print(f"Erreur statut abonnement: {e}")
        return jsonify({'error': 'Erreur lors de la récupération du statut'}), 500

@payment_bp.route('/upgrade', methods=['POST'])
@jwt_required()
def upgrade_subscription():
    """
    Met à niveau l'abonnement de l'utilisateur
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        new_package_id = data.get('package_id')
        
        # Vérifier que le package existe
        packages = payment_service.get_pricing_packages()
        selected_package = next((p for p in packages if p['id'] == new_package_id), None)
        
        if not selected_package:
            return jsonify({'error': 'Package non trouvé'}), 404
        
        # Créer le paiement de mise à niveau
        payment_data = payment_service.create_payment(
            amount=selected_package['price'],
            user_id=str(user_id),
            description=f"Mise à niveau vers {selected_package['name']} - AgroBizChat",
            phone_number=None,  # À récupérer de l'utilisateur
            email=None  # À récupérer de l'utilisateur
        )
        
        if payment_data:
            return jsonify({
                'success': True,
                'payment_data': payment_data,
                'package': selected_package
            })
        else:
            return jsonify({'error': 'Erreur lors de la création du paiement'}), 500
        
    except Exception as e:
        print(f"Erreur mise à niveau: {e}")
        return jsonify({'error': 'Erreur lors de la mise à niveau'}), 500

def create_subscription(user_id: int, package_id: str):
    """
    Crée un abonnement pour l'utilisateur
    
    Args:
        user_id (int): ID de l'utilisateur
        package_id (str): ID du package
    """
    try:
        # Désactiver l'abonnement précédent s'il existe
        existing_subscription = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if existing_subscription:
            existing_subscription.status = 'cancelled'
            existing_subscription.updated_at = datetime.now()
        
        # Déterminer la durée selon le package
        duration_days = {
            'basic': 30,
            'premium': 30,
            'cooperative': 30
        }.get(package_id, 30)
        
        # Créer le nouvel abonnement
        subscription = Subscription(
            user_id=user_id,
            package_id=package_id,
            status='active',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=duration_days),
            created_at=datetime.now()
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        print(f"Abonnement créé pour utilisateur {user_id}, package {package_id}")
        
    except Exception as e:
        print(f"Erreur création abonnement: {e}")
        db.session.rollback()

def get_package_features(package_id: str) -> dict:
    """
    Retourne les fonctionnalités d'un package
    
    Args:
        package_id (str): ID du package
        
    Returns:
        dict: Fonctionnalités du package
    """
    features = {
        'free': {
            'business_plan_basic': True,
            'weather_basic': True,
            'chat_support': True,
            'diagnosis_photo': False,
            'pdf_premium': False,
            'cooperative_features': False
        },
        'basic': {
            'business_plan_basic': True,
            'weather_basic': True,
            'chat_support': True,
            'diagnosis_photo': False,
            'pdf_premium': True,
            'cooperative_features': False
        },
        'premium': {
            'business_plan_basic': True,
            'weather_basic': True,
            'chat_support': True,
            'diagnosis_photo': True,
            'pdf_premium': True,
            'cooperative_features': False
        },
        'cooperative': {
            'business_plan_basic': True,
            'weather_basic': True,
            'chat_support': True,
            'diagnosis_photo': True,
            'pdf_premium': True,
            'cooperative_features': True
        }
    }
    
    return features.get(package_id, features['free'])

@payment_bp.route('/test-payment', methods=['POST'])
def test_payment():
    """
    Endpoint de test pour simuler un paiement (développement uniquement)
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        package_id = data.get('package_id', 'basic')
        
        if not user_id:
            return jsonify({'error': 'User ID requis'}), 400
        
        # Créer un abonnement de test
        create_subscription(user_id, package_id)
        
        return jsonify({
            'success': True,
            'message': f'Abonnement de test créé pour package {package_id}',
            'features': get_package_features(package_id)
        })
        
    except Exception as e:
        print(f"Erreur test paiement: {e}")
        return jsonify({'error': 'Erreur lors du test'}), 500 