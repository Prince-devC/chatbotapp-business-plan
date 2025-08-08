"""
Service de paiement pour AgroBizChat
Intégration avec Kkiapay et PayDunya
"""

import requests
import json
import hashlib
import hmac
from typing import Dict, Optional, List
from datetime import datetime

class PaymentService:
    """Service pour gérer les paiements en FCFA"""
    
    def __init__(self, provider: str = "kkiapay", api_key: str = None, secret_key: str = None):
        self.provider = provider
        self.api_key = api_key
        self.secret_key = secret_key
        
        # Configuration des providers
        self.providers_config = {
            "kkiapay": {
                "base_url": "https://api.kkiapay.com",
                "sandbox_url": "https://api-sandbox.kkiapay.com"
            },
            "paydunya": {
                "base_url": "https://api.paydunya.com",
                "sandbox_url": "https://api-sandbox.paydunya.com"
            }
        }
        
        self.base_url = self.providers_config[provider]["base_url"]
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
    
    def create_payment(self, amount: int, user_id: str, description: str, 
                      phone_number: str = None, email: str = None) -> Optional[Dict]:
        """
        Crée une transaction de paiement
        
        Args:
            amount (int): Montant en FCFA
            user_id (str): ID de l'utilisateur
            description (str): Description du paiement
            phone_number (str): Numéro de téléphone
            email (str): Email
            
        Returns:
            dict: Informations de paiement ou None si erreur
        """
        try:
            if self.provider == "kkiapay":
                return self._create_kkiapay_payment(amount, user_id, description, phone_number, email)
            elif self.provider == "paydunya":
                return self._create_paydunya_payment(amount, user_id, description, phone_number, email)
            else:
                raise ValueError(f"Provider non supporté: {self.provider}")
                
        except Exception as e:
            print(f"Erreur lors de la création du paiement: {e}")
            return None
    
    def _create_kkiapay_payment(self, amount: int, user_id: str, description: str,
                               phone_number: str = None, email: str = None) -> Optional[Dict]:
        """
        Crée un paiement via Kkiapay
        
        Args:
            amount (int): Montant en FCFA
            user_id (str): ID de l'utilisateur
            description (str): Description
            phone_number (str): Numéro de téléphone
            email (str): Email
            
        Returns:
            dict: Informations de paiement
        """
        payload = {
            "amount": amount,
            "currency": "XOF",
            "description": description,
            "reference": f"agrobiz_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "callback_url": f"{self.base_url}/webhook/payment/callback",
            "return_url": f"{self.base_url}/payment/success",
            "cancel_url": f"{self.base_url}/payment/cancel"
        }
        
        if phone_number:
            payload["phone"] = phone_number
        if email:
            payload["email"] = email
        
        response = self.session.post(
            f"{self.base_url}/api/v1/transactions/initialize",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "payment_id": data.get("id"),
                "payment_url": data.get("payment_url"),
                "reference": payload["reference"],
                "amount": amount,
                "status": "pending"
            }
        else:
            print(f"Erreur Kkiapay: {response.status_code}")
            return None
    
    def _create_paydunya_payment(self, amount: int, user_id: str, description: str,
                                phone_number: str = None, email: str = None) -> Optional[Dict]:
        """
        Crée un paiement via PayDunya
        
        Args:
            amount (int): Montant en FCFA
            user_id (str): ID de l'utilisateur
            description (str): Description
            phone_number (str): Numéro de téléphone
            email (str): Email
            
        Returns:
            dict: Informations de paiement
        """
        payload = {
            "invoice": {
                "items": [
                    {
                        "name": description,
                        "quantity": 1,
                        "unit_price": amount,
                        "total_price": amount,
                        "description": description
                    }
                ],
                "total_amount": amount,
                "description": description
            },
            "store": {
                "name": "AgroBizChat"
            },
            "custom_data": {
                "user_id": user_id
            },
            "actions": {
                "callback_url": f"{self.base_url}/webhook/payment/callback",
                "return_url": f"{self.base_url}/payment/success",
                "cancel_url": f"{self.base_url}/payment/cancel"
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/checkout-invoice/create",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "payment_id": data.get("token"),
                "payment_url": data.get("receipt_url"),
                "reference": data.get("invoice", {}).get("reference"),
                "amount": amount,
                "status": "pending"
            }
        else:
            print(f"Erreur PayDunya: {response.status_code}")
            return None
    
    def verify_payment(self, payment_id: str) -> Optional[Dict]:
        """
        Vérifie le statut d'un paiement
        
        Args:
            payment_id (str): ID du paiement
            
        Returns:
            dict: Statut du paiement ou None si erreur
        """
        try:
            if self.provider == "kkiapay":
                return self._verify_kkiapay_payment(payment_id)
            elif self.provider == "paydunya":
                return self._verify_paydunya_payment(payment_id)
            else:
                raise ValueError(f"Provider non supporté: {self.provider}")
                
        except Exception as e:
            print(f"Erreur lors de la vérification: {e}")
            return None
    
    def _verify_kkiapay_payment(self, payment_id: str) -> Optional[Dict]:
        """
        Vérifie un paiement Kkiapay
        
        Args:
            payment_id (str): ID du paiement
            
        Returns:
            dict: Statut du paiement
        """
        response = self.session.get(
            f"{self.base_url}/api/v1/transactions/{payment_id}"
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "payment_id": payment_id,
                "status": data.get("status"),
                "amount": data.get("amount"),
                "reference": data.get("reference"),
                "paid_at": data.get("paid_at")
            }
        else:
            print(f"Erreur vérification Kkiapay: {response.status_code}")
            return None
    
    def _verify_paydunya_payment(self, payment_id: str) -> Optional[Dict]:
        """
        Vérifie un paiement PayDunya
        
        Args:
            payment_id (str): ID du paiement
            
        Returns:
            dict: Statut du paiement
        """
        response = self.session.get(
            f"{self.base_url}/api/v1/checkout-invoice/confirm/{payment_id}"
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "payment_id": payment_id,
                "status": data.get("status"),
                "amount": data.get("invoice", {}).get("total_amount"),
                "reference": data.get("invoice", {}).get("reference"),
                "paid_at": data.get("paid_at")
            }
        else:
            print(f"Erreur vérification PayDunya: {response.status_code}")
            return None
    
    def get_pricing_packages(self) -> List[Dict]:
        """
        Retourne les packages de prix disponibles
        
        Returns:
            list: Liste des packages
        """
        return [
            {
                "id": "basic",
                "name": "Pack Basique",
                "price": 500,
                "currency": "XOF",
                "features": [
                    "Génération de business plan PDF",
                    "Conseils météo de base",
                    "Support WhatsApp"
                ]
            },
            {
                "id": "premium",
                "name": "Pack Premium",
                "price": 1500,
                "currency": "XOF",
                "features": [
                    "Génération de business plan PDF + Excel",
                    "Diagnostic maladies par photo",
                    "Conseils météo avancés",
                    "Conseils post-récolte",
                    "Support WhatsApp + Telegram"
                ]
            },
            {
                "id": "cooperative",
                "name": "Pack Coopérative",
                "price": 3000,
                "currency": "XOF",
                "features": [
                    "Toutes les fonctionnalités Premium",
                    "Plans collectifs",
                    "Rapports groupés",
                    "Fournisseurs adaptés volume",
                    "Support prioritaire"
                ]
            }
        ]
    
    def process_webhook(self, webhook_data: Dict, signature: str = None) -> Optional[Dict]:
        """
        Traite un webhook de paiement
        
        Args:
            webhook_data (dict): Données du webhook
            signature (str): Signature pour vérification
            
        Returns:
            dict: Données traitées ou None si invalide
        """
        try:
            # Vérification de la signature si fournie
            if signature and not self._verify_signature(webhook_data, signature):
                print("Signature webhook invalide")
                return None
            
            # Extraction des données selon le provider
            if self.provider == "kkiapay":
                return self._process_kkiapay_webhook(webhook_data)
            elif self.provider == "paydunya":
                return self._process_paydunya_webhook(webhook_data)
            else:
                return webhook_data
                
        except Exception as e:
            print(f"Erreur traitement webhook: {e}")
            return None
    
    def _verify_signature(self, data: Dict, signature: str) -> bool:
        """
        Vérifie la signature du webhook
        
        Args:
            data (dict): Données du webhook
            signature (str): Signature reçue
            
        Returns:
            bool: True si signature valide
        """
        if not self.secret_key:
            return True  # Pas de vérification si pas de clé secrète
        
        # Création de la signature attendue
        message = json.dumps(data, sort_keys=True)
        expected_signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def _process_kkiapay_webhook(self, data: Dict) -> Dict:
        """
        Traite un webhook Kkiapay
        
        Args:
            data (dict): Données du webhook
            
        Returns:
            dict: Données traitées
        """
        return {
            "payment_id": data.get("id"),
            "status": data.get("status"),
            "amount": data.get("amount"),
            "reference": data.get("reference"),
            "user_id": data.get("metadata", {}).get("user_id"),
            "provider": "kkiapay"
        }
    
    def _process_paydunya_webhook(self, data: Dict) -> Dict:
        """
        Traite un webhook PayDunya
        
        Args:
            data (dict): Données du webhook
            
        Returns:
            dict: Données traitées
        """
        return {
            "payment_id": data.get("token"),
            "status": data.get("status"),
            "amount": data.get("invoice", {}).get("total_amount"),
            "reference": data.get("invoice", {}).get("reference"),
            "user_id": data.get("custom_data", {}).get("user_id"),
            "provider": "paydunya"
        } 