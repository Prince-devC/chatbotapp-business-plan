#!/usr/bin/env python3
"""
Test du webhook WhatsApp avec différents formats
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"  # Ajustez selon votre configuration

def test_whatsapp_webhook_form_data():
    """Test avec le format form data (Twilio)"""
    print("🧪 Test webhook WhatsApp - Format Form Data (Twilio)")
    
    # Données de test Twilio
    form_data = {
        'MessageSid': 'MSG123456789',
        'From': 'whatsapp:+1234567890',
        'Body': 'Je veux faire du maïs sur 5 hectares',
        'To': 'whatsapp:+14155238886',
        'AccountSid': 'AC123456789'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook/whatsapp",
            data=form_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        if response.status_code == 200 or response.status_code == 204:
            print("✅ Test form data réussi")
        else:
            print("❌ Test form data échoué")
            
    except Exception as e:
        print(f"❌ Erreur test form data: {e}")

def test_whatsapp_webhook_json():
    """Test avec le format JSON (WhatsApp Business API)"""
    print("\n🧪 Test webhook WhatsApp - Format JSON (WhatsApp Business API)")
    
    # Données de test WhatsApp Business API
    json_data = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "123456789",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "1234567890",
                        "phone_number_id": "123456789"
                    },
                    "messages": [{
                        "id": "MSG123456789",
                        "from": "1234567890",
                        "timestamp": "1234567890",
                        "type": "text",
                        "text": {
                            "body": "Je veux faire du maïs sur 5 hectares"
                        }
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook/whatsapp",
            json=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        if response.status_code == 200 or response.status_code == 204:
            print("✅ Test JSON réussi")
        else:
            print("❌ Test JSON échoué")
            
    except Exception as e:
        print(f"❌ Erreur test JSON: {e}")

def test_whatsapp_webhook_simple_json():
    """Test avec un format JSON simplifié"""
    print("\n🧪 Test webhook WhatsApp - Format JSON simplifié")
    
    # Format JSON simplifié
    json_data = {
        "Body": "Je veux faire du maïs sur 5 hectares",
        "From": "1234567890",
        "MessageSid": "MSG123456789"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook/whatsapp",
            json=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        if response.status_code == 200 or response.status_code == 204:
            print("✅ Test JSON simplifié réussi")
        else:
            print("❌ Test JSON simplifié échoué")
            
    except Exception as e:
        print(f"❌ Erreur test JSON simplifié: {e}")

def test_whatsapp_gemini_webhook():
    """Test du webhook WhatsApp Gemini"""
    print("\n🧪 Test webhook WhatsApp Gemini")
    
    # Données de test pour le webhook Gemini
    json_data = {
        "Body": "Je veux faire du maïs sur 5 hectares",
        "From": "1234567890"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook/whatsapp-gemini",
            json=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Test webhook Gemini réussi")
        else:
            print("❌ Test webhook Gemini échoué")
            
    except Exception as e:
        print(f"❌ Erreur test webhook Gemini: {e}")

if __name__ == "__main__":
    print("🚀 Tests du webhook WhatsApp")
    print("=" * 50)
    
    # Tests
    test_whatsapp_webhook_form_data()
    test_whatsapp_webhook_json()
    test_whatsapp_webhook_simple_json()
    test_whatsapp_gemini_webhook()
    
    print("\n�� Tests terminés !") 