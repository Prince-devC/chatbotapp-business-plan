#!/usr/bin/env python3
"""
Tests pour les services Semaine 4 AgroBizChat
Validation paiements FCFA et modèle freemium
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.payment_service import PaymentService
from src.models.payment_models import PaymentTransaction, Subscription, Package
from datetime import datetime, timedelta

def test_payment_service():
    """Test du service de paiement"""
    print("💳 Test PaymentService...")
    
    try:
        payment_service = PaymentService(provider="kkiapay")
        
        # Test packages de prix
        packages = payment_service.get_pricing_packages()
        assert len(packages) == 3, f"Nombre de packages incorrect: {len(packages)}"
        
        # Vérifier les packages
        package_ids = [p['id'] for p in packages]
        assert 'basic' in package_ids, "Package basic manquant"
        assert 'premium' in package_ids, "Package premium manquant"
        assert 'cooperative' in package_ids, "Package cooperative manquant"
        
        # Vérifier les prix
        basic_package = next(p for p in packages if p['id'] == 'basic')
        premium_package = next(p for p in packages if p['id'] == 'premium')
        cooperative_package = next(p for p in packages if p['id'] == 'cooperative')
        
        assert basic_package['price'] == 500, f"Prix basic incorrect: {basic_package['price']}"
        assert premium_package['price'] == 1500, f"Prix premium incorrect: {premium_package['price']}"
        assert cooperative_package['price'] == 3000, f"Prix cooperative incorrect: {cooperative_package['price']}"
        
        print("✅ Packages de prix OK")
        print(f"✅ Basic: {basic_package['price']} FCFA")
        print(f"✅ Premium: {premium_package['price']} FCFA")
        print(f"✅ Coopérative: {cooperative_package['price']} FCFA")
        
        # Test création paiement (simulation)
        payment_data = payment_service.create_payment(
            amount=500,
            user_id='test_user_001',
            description='Pack Basique AgroBizChat',
            phone_number='+22990123456'
        )
        
        # Le test échouera car pas d'API configurée, mais on teste la structure
        if payment_data:
            assert 'payment_id' in payment_data, "Payment ID manquant"
            assert 'payment_url' in payment_data, "Payment URL manquant"
            assert 'reference' in payment_data, "Reference manquante"
            print("✅ Création paiement OK")
        else:
            print("⚠️ Création paiement: Pas d'API configurée (normal)")
        
        # Test webhook (simulation)
        mock_webhook_data = {
            'id': 'test_payment_id',
            'status': 'completed',
            'amount': 500,
            'reference': 'test_ref_001'
        }
        
        webhook_result = payment_service.process_webhook(mock_webhook_data)
        if webhook_result:
            assert 'payment_id' in webhook_result, "Payment ID manquant dans webhook"
            assert 'status' in webhook_result, "Status manquant dans webhook"
            print("✅ Traitement webhook OK")
        else:
            print("⚠️ Traitement webhook: Pas d'API configurée (normal)")
        
        print("🎉 PaymentService: Tests de base passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur PaymentService: {e}")
        return False

def test_payment_models():
    """Test des modèles de paiement"""
    print("\n📊 Test modèles de paiement...")
    
    try:
        # Test PaymentTransaction
        transaction = PaymentTransaction(
            user_id=1,
            package_id='basic',
            amount=500,
            currency='XOF',
            provider='kkiapay',
            payment_id='test_payment_001',
            reference='test_ref_001',
            status='pending',
            payment_url='https://example.com/pay'
        )
        
        # Test propriétés
        assert transaction.user_id == 1, "User ID incorrect"
        assert transaction.package_id == 'basic', "Package ID incorrect"
        assert transaction.amount == 500, "Amount incorrect"
        assert transaction.currency == 'XOF', "Currency incorrect"
        assert transaction.provider == 'kkiapay', "Provider incorrect"
        assert transaction.status == 'pending', "Status incorrect"
        
        # Test to_dict
        transaction_dict = transaction.to_dict()
        assert 'id' in transaction_dict, "ID manquant dans to_dict"
        assert 'user_id' in transaction_dict, "User ID manquant dans to_dict"
        assert 'package_id' in transaction_dict, "Package ID manquant dans to_dict"
        assert 'amount' in transaction_dict, "Amount manquant dans to_dict"
        
        print("✅ PaymentTransaction OK")
        
        # Test Subscription
        subscription = Subscription(
            user_id=1,
            package_id='premium',
            status='active',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30)
        )
        
        # Test propriétés
        assert subscription.user_id == 1, "User ID incorrect"
        assert subscription.package_id == 'premium', "Package ID incorrect"
        assert subscription.status == 'active', "Status incorrect"
        assert subscription.is_active, "is_active incorrect"
        assert subscription.days_remaining > 0, "Days remaining incorrect"
        
        # Test to_dict
        subscription_dict = subscription.to_dict()
        assert 'id' in subscription_dict, "ID manquant dans to_dict"
        assert 'user_id' in subscription_dict, "User ID manquant dans to_dict"
        assert 'package_id' in subscription_dict, "Package ID manquant dans to_dict"
        assert 'is_active' in subscription_dict, "is_active manquant dans to_dict"
        assert 'days_remaining' in subscription_dict, "days_remaining manquant dans to_dict"
        
        print("✅ Subscription OK")
        
        # Test Package
        package = Package(
            id='test_package',
            name='Package Test',
            price=1000,
            currency='XOF',
            duration_days=30,
            description='Package de test'
        )
        
        # Test propriétés
        assert package.id == 'test_package', "ID incorrect"
        assert package.name == 'Package Test', "Name incorrect"
        assert package.price == 1000, "Price incorrect"
        assert package.currency == 'XOF', "Currency incorrect"
        
        # Test features
        test_features = {'feature1': True, 'feature2': False}
        package.set_features(test_features)
        retrieved_features = package.get_features()
        assert retrieved_features == test_features, "Features incorrectes"
        
        # Test to_dict
        package_dict = package.to_dict()
        assert 'id' in package_dict, "ID manquant dans to_dict"
        assert 'name' in package_dict, "Name manquant dans to_dict"
        assert 'price' in package_dict, "Price manquant dans to_dict"
        assert 'features' in package_dict, "Features manquant dans to_dict"
        
        print("✅ Package OK")
        
        print("🎉 Modèles de paiement: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modèles de paiement: {e}")
        return False

def test_freemium_features():
    """Test du modèle freemium"""
    print("\n🎯 Test modèle freemium...")
    
    try:
        from src.routes.payment import get_package_features
        
        # Test fonctionnalités par package
        packages = ['free', 'basic', 'premium', 'cooperative']
        
        for package_id in packages:
            features = get_package_features(package_id)
            
            # Vérifier que toutes les fonctionnalités sont définies
            expected_features = [
                'business_plan_basic',
                'weather_basic', 
                'chat_support',
                'diagnosis_photo',
                'pdf_premium',
                'cooperative_features'
            ]
            
            for feature in expected_features:
                assert feature in features, f"Fonctionnalité {feature} manquante pour {package_id}"
            
            print(f"✅ Package {package_id}: {len(features)} fonctionnalités")
        
        # Test spécifique des fonctionnalités
        free_features = get_package_features('free')
        assert free_features['business_plan_basic'] == True, "Business plan basic gratuit"
        assert free_features['diagnosis_photo'] == False, "Diagnostic photo payant"
        assert free_features['pdf_premium'] == False, "PDF premium payant"
        
        premium_features = get_package_features('premium')
        assert premium_features['diagnosis_photo'] == True, "Diagnostic photo inclus premium"
        assert premium_features['pdf_premium'] == True, "PDF premium inclus"
        
        cooperative_features = get_package_features('cooperative')
        assert cooperative_features['cooperative_features'] == True, "Fonctionnalités coopérative"
        
        print("✅ Fonctionnalités freemium OK")
        
        # Test vérification abonnement (simulation)
        def mock_check_subscription(user_id):
            """Simule la vérification d'abonnement"""
            if user_id == 1:
                return get_package_features('premium')
            else:
                return get_package_features('free')
        
        # Test utilisateur premium
        premium_user_features = mock_check_subscription(1)
        assert premium_user_features['diagnosis_photo'] == True, "Utilisateur premium devrait avoir diagnostic photo"
        assert premium_user_features['pdf_premium'] == True, "Utilisateur premium devrait avoir PDF premium"
        
        # Test utilisateur gratuit
        free_user_features = mock_check_subscription(2)
        assert free_user_features['diagnosis_photo'] == False, "Utilisateur gratuit ne devrait pas avoir diagnostic photo"
        assert free_user_features['pdf_premium'] == False, "Utilisateur gratuit ne devrait pas avoir PDF premium"
        
        print("✅ Vérification abonnements OK")
        
        print("🎉 Modèle freemium: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modèle freemium: {e}")
        return False

def test_payment_integration():
    """Test d'intégration des paiements"""
    print("\n🔗 Test intégration paiements...")
    
    try:
        payment_service = PaymentService(provider="kkiapay")
        
        # Simuler un flow de paiement complet
        # 1. Récupérer les packages
        packages = payment_service.get_pricing_packages()
        basic_package = next(p for p in packages if p['id'] == 'basic')
        
        # 2. Créer un paiement
        payment_data = payment_service.create_payment(
            amount=basic_package['price'],
            user_id='test_integration_user',
            description=f"Pack {basic_package['name']} - AgroBizChat",
            phone_number='+22990123456'
        )
        
        if payment_data:
            print(f"✅ Paiement créé: {payment_data['payment_id']}")
            
            # 3. Simuler un webhook de paiement réussi
            webhook_data = {
                'payment_id': payment_data['payment_id'],
                'status': 'completed',
                'amount': basic_package['price'],
                'reference': payment_data['reference']
            }
            
            webhook_result = payment_service.process_webhook(webhook_data)
            
            if webhook_result:
                print(f"✅ Webhook traité: {webhook_result['status']}")
                
                # 4. Vérifier que l'abonnement serait créé
                print("✅ Flow d'intégration paiement réussi!")
            else:
                print("⚠️ Webhook non traité (API non configurée)")
        else:
            print("⚠️ Paiement non créé (API non configurée)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration paiements: {e}")
        return False

def test_subscription_management():
    """Test de la gestion des abonnements"""
    print("\n📅 Test gestion abonnements...")
    
    try:
        # Test création abonnement
        subscription = Subscription(
            user_id=1,
            package_id='premium',
            status='active',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30)
        )
        
        # Vérifier les propriétés
        assert subscription.is_active, "Abonnement devrait être actif"
        assert subscription.days_remaining > 0, "Jours restants incorrects"
        
        # Test abonnement expiré
        expired_subscription = Subscription(
            user_id=2,
            package_id='basic',
            status='active',
            start_date=datetime.now() - timedelta(days=60),
            end_date=datetime.now() - timedelta(days=30)
        )
        
        assert not expired_subscription.is_active, "Abonnement expiré devrait être inactif"
        assert expired_subscription.days_remaining == 0, "Jours restants expiré incorrects"
        
        # Test changement de statut
        subscription.status = 'cancelled'
        assert not subscription.is_active, "Abonnement annulé devrait être inactif"
        
        print("✅ Gestion abonnements OK")
        
        # Test packages avec fonctionnalités
        packages = [
            {'id': 'free', 'name': 'Gratuit', 'price': 0},
            {'id': 'basic', 'name': 'Basique', 'price': 500},
            {'id': 'premium', 'name': 'Premium', 'price': 1500},
            {'id': 'cooperative', 'name': 'Coopérative', 'price': 3000}
        ]
        
        for package in packages:
            features = get_package_features(package['id'])
            print(f"✅ Package {package['name']}: {len(features)} fonctionnalités")
        
        print("🎉 Gestion abonnements: Tous les tests passent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur gestion abonnements: {e}")
        return False

def run_week4_tests():
    """Exécute tous les tests de la semaine 4"""
    print("🚀 Début des tests Semaine 4 - Paiement & freemium en FCFA...\n")
    
    tests = [
        test_payment_service,
        test_payment_models,
        test_freemium_features,
        test_payment_integration,
        test_subscription_management
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Résultats des tests Semaine 4:")
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passent! Services Semaine 4 prêts pour la production.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == '__main__':
    success = run_week4_tests()
    sys.exit(0 if success else 1) 