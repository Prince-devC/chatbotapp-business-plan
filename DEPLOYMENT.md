# 🚀 Guide de Déploiement - Chatbot Business Plan

## ✅ Corrections apportées pour la production

### 1. **Dependencies (requirements.txt)**
- ✅ Versions compatibles sans conflits
- ✅ Ajout de `cryptography` et `twilio`
- ✅ Ajout de `gunicorn` pour la production

### 2. **Configuration dynamique (src/main.py)**
- ✅ Port dynamique via `os.environ.get('PORT', 5000)`
- ✅ Mode debug conditionnel selon `FLASK_ENV`
- ✅ Chemins absolus pour les fichiers générés

### 3. **URLs dynamiques (src/static/index.html)**
- ✅ `window.location.origin` au lieu de `127.0.0.1:5000`
- ✅ APIs dynamiques pour tous les endpoints
- ✅ URLs de téléchargement relatives

### 4. **Fichiers de déploiement**
- ✅ `Procfile` avec Gunicorn
- ✅ `runtime.txt` pour Python 3.11
- ✅ `railway.json` pour Railway
- ✅ `.dockerignore` pour optimiser le build

### 5. **Chemins des fichiers**
- ✅ `DocumentGenerator` utilise des chemins absolus
- ✅ Route `/download/` avec chemins absolus
- ✅ Service WhatsApp avec URLs dynamiques

## 🚀 Options de déploiement gratuit

### Option 1: Railway (Recommandée)
```bash
# Installation
npm install -g @railway/cli

# Connexion
railway login

# Initialisation
railway init

# Déploiement
railway up

# Ou utiliser le script
./deploy.sh
```

### Option 2: Render
1. Créer un compte sur [render.com](https://render.com)
2. Connecter votre repo GitHub
3. Créer un nouveau "Web Service"
4. Configuration automatique détectée

### Option 3: Heroku
```bash
# Installation Heroku CLI
brew install heroku/brew/heroku

# Connexion
heroku login

# Création app
heroku create votre-app-name

# Déploiement
git push heroku main
```

## 🔧 Variables d'environnement à configurer

```env
# Flask
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
FLASK_ENV=production

# AI
GEMINI_API_KEY=your-real-gemini-api-key

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Webhook
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your-verify-token
```

## 📱 Configuration WhatsApp

1. **URL Webhook**: `https://votre-domaine.com/webhook/whatsapp`
2. **Verify Token**: Utiliser la valeur de `WHATSAPP_WEBHOOK_VERIFY_TOKEN`
3. **Test**: Envoyer `/start` puis "Je veux créer une startup"

## 🧪 Test local avant déploiement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement
export FLASK_ENV=production
export PORT=5000

# Test avec Gunicorn (comme en production)
gunicorn --bind 0.0.0.0:5000 --workers 1 src.main:app

# Test endpoints
curl http://localhost:5000/health
curl -X POST http://localhost:5000/api/chatbot/test-gemini \
  -H "Content-Type: application/json" \
  -d '{"message": "Je veux créer une startup de livraison", "phone": "test"}'
```

## 🎯 URLs importantes après déploiement

- **Dashboard**: `https://votre-domaine.com/`
- **Health Check**: `https://votre-domaine.com/health`
- **Webhook WhatsApp**: `https://votre-domaine.com/webhook/whatsapp`
- **API Documentation**: `https://votre-domaine.com/api/`

## 🔍 Monitoring

```bash
# Railway logs
railway logs

# Heroku logs
heroku logs --tail

# Render logs
# Via dashboard web
```

## ⚡ Performance

- ✅ SQLite database (pas de config DB externe)
- ✅ Fichiers statiques servis par Flask
- ✅ Gunicorn avec 1 worker (gratuit)
- ✅ Templates analysés en cache mémoire
- ✅ Génération documents optimisée

## 🛠️ Dépannage

### Erreur de démarrage
- Vérifier les variables d'environnement
- Vérifier les logs de déploiement
- Tester en local avec les mêmes configs

### Webhook WhatsApp ne répond pas
- Vérifier l'URL webhook dans Twilio
- Vérifier le verify token
- Tester avec `/start` puis "Je veux..."

### Fichiers non générés
- Vérifier les permissions d'écriture
- Vérifier l'espace disque
- Vérifier les logs d'erreur

## 🎉 Fonctionnalités en production

✅ **Mode démo** activé automatiquement sans clé Gemini  
✅ **Analyse de templates** de la base de données  
✅ **Génération Excel + PDF** basée sur templates  
✅ **WhatsApp automatique** avec commandes `/start` et "Je veux"  
✅ **Dashboard web** pour gestion des templates  
✅ **Téléchargements** sécurisés des business plans  

---

🚀 **Votre application est maintenant prête pour la production !** 