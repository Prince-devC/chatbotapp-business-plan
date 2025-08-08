# 🔧 Guide de Dépannage - Webhook WhatsApp

## 🚨 Erreur 415 Unsupported Media Type

### Problème
```
Erreur webhook WhatsApp: 415 Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not 'application/json'.
```

### Cause
Le webhook WhatsApp reçoit des données avec un Content-Type différent de celui attendu par le code.

### Solutions

#### 1. ✅ Solution Implémentée (Recommandée)

Le webhook a été mis à jour pour gérer automatiquement les deux formats :

**Format Form Data (Twilio) :**
```bash
curl -X POST "https://votre-domaine.com/webhook/whatsapp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "MessageSid=MSG123456789&From=whatsapp:+1234567890&Body=Je veux faire du maïs"
```

**Format JSON (WhatsApp Business API) :**
```bash
curl -X POST "https://votre-domaine.com/webhook/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "Body": "Je veux faire du maïs",
    "From": "1234567890",
    "MessageSid": "MSG123456789"
  }'
```

#### 2. 🔧 Configuration Twilio

Si vous utilisez Twilio, configurez le webhook avec :

**URL :** `https://votre-domaine.com/webhook/whatsapp`
**HTTP Method :** POST
**Content Type :** `application/x-www-form-urlencoded`

#### 3. 🔧 Configuration WhatsApp Business API

Si vous utilisez WhatsApp Business API, configurez le webhook avec :

**URL :** `https://votre-domaine.com/webhook/whatsapp`
**HTTP Method :** POST
**Content Type :** `application/json`

### 🧪 Tests

Utilisez le script de test pour vérifier le fonctionnement :

```bash
python test_webhook_whatsapp.py
```

### 📋 Formats Supportés

#### Format 1 : Twilio (Form Data)
```python
{
    'MessageSid': 'MSG123456789',
    'From': 'whatsapp:+1234567890',
    'Body': 'Je veux faire du maïs sur 5 hectares',
    'To': 'whatsapp:+14155238886'
}
```

#### Format 2 : WhatsApp Business API (JSON)
```python
{
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "123456789",
        "changes": [{
            "value": {
                "messaging_product": "whatsapp",
                "messages": [{
                    "id": "MSG123456789",
                    "from": "1234567890",
                    "type": "text",
                    "text": {
                        "body": "Je veux faire du maïs sur 5 hectares"
                    }
                }]
            }
        }]
    }]
}
```

#### Format 3 : Simplifié (JSON)
```python
{
    "Body": "Je veux faire du maïs sur 5 hectares",
    "From": "1234567890",
    "MessageSid": "MSG123456789"
}
```

### 🔍 Debugging

#### 1. Vérifier les Logs
```bash
# Vérifier les logs de l'application
tail -f logs/app.log
```

#### 2. Tester avec curl
```bash
# Test form data
curl -X POST "http://localhost:5000/webhook/whatsapp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=Test message&From=1234567890"

# Test JSON
curl -X POST "http://localhost:5000/webhook/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{"Body": "Test message", "From": "1234567890"}'
```

#### 3. Vérifier la Configuration
```python
# Dans votre code, ajoutez des logs de debug
print(f"Content-Type: {request.content_type}")
print(f"Data: {request.get_data()}")
```

### 🛠️ Configuration Serveur

#### Nginx
```nginx
location /webhook/whatsapp {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

#### Apache
```apache
<Location "/webhook/whatsapp">
    ProxyPass http://localhost:5000
    ProxyPassReverse http://localhost:5000
</Location>
```

### 📞 Support

Si le problème persiste :

1. ✅ Vérifiez que l'application est démarrée
2. ✅ Vérifiez les logs d'erreur
3. ✅ Testez avec le script de test
4. ✅ Vérifiez la configuration du provider WhatsApp
5. 📧 Contactez le support technique

### 🔄 Mise à Jour

Le webhook a été mis à jour pour :
- ✅ Gérer automatiquement les deux formats (form data et JSON)
- ✅ Détecter le Content-Type automatiquement
- ✅ Supporter les différents providers WhatsApp
- ✅ Améliorer la gestion d'erreurs 