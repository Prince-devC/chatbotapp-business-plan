# 🚀 Déploiement Rapide - AgroBiz Chatbot

## ⚡ **Démarrage en 3 étapes**

### 1. **Test de Configuration**
```bash
# Vérifier que tout est prêt
python test_deployment.py
```

### 2. **Déploiement Automatique**
```bash
# Script principal avec choix de plateforme
./deploy.sh

# Ou directement sur Render (recommandé)
./deploy_render.sh
```

### 3. **Configuration des Variables**
Configurez vos clés API sur la plateforme choisie.

---

## 🎯 **Plateformes Disponibles**

| Plateforme | Script | Avantages |
|------------|--------|-----------|
| **Render** | `./deploy_render.sh` | ✅ Gratuit, Simple, PostgreSQL |
| **Heroku** | `./deploy_heroku.sh` | ✅ Gratuit, Populaire |
| **Vercel** | `./deploy_vercel.sh` | ✅ Gratuit, Rapide |

---

## 🔑 **Variables d'Environnement Requises**

```bash
# Gemini AI
GEMINI_API_KEY=your_gemini_key

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_whatsapp_number

# Optionnel
TELEGRAM_BOT_TOKEN=your_telegram_token
```

---

## 📋 **Commandes Utiles**

```bash
# Rendre les scripts exécutables
chmod +x *.sh

# Test de configuration
python test_deployment.py

# Déploiement avec choix
./deploy.sh

# Déploiement direct Render
./deploy_render.sh

# Déploiement direct Heroku
./deploy_heroku.sh

# Déploiement direct Vercel
./deploy_vercel.sh
```

---

## 🌐 **URLs de Déploiement**

- **Render** : `https://agrobiz-chatbot.onrender.com`
- **Heroku** : `https://your-app-name.herokuapp.com`
- **Vercel** : `https://your-app-name.vercel.app`

---

## 📚 **Documentation Complète**

Consultez `DEPLOYMENT_ALTERNATIVES.md` pour tous les détails et le troubleshooting. 