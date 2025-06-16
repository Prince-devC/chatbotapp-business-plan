# Chatbot Business Plan

Un chatbot multiplateforme (Telegram, WhatsApp) pour la génération et la gestion de business plans.

## 📋 Description

Ce projet est une application Flask qui permet de générer des business plans via une interface conversationnelle. Il supporte plusieurs plateformes de messagerie et offre une gestion complète des templates de business plans.

## 🚀 Fonctionnalités

- 💬 Support multiplateforme :
  - Telegram
  - WhatsApp (via Twilio)
- 📝 Génération de business plans
- 📊 Analyse de marché
- 💼 Gestion des templates
- 👥 Gestion des utilisateurs
- 🔒 Interface d'administration sécurisée
- 📤 Export en plusieurs formats (PDF, HTML, TXT)

## 🛠 Prérequis

- Python 3.11+
- Flask
- SQLite3
- Compte Telegram Bot
- Compte Twilio (pour WhatsApp)
- WeasyPrint (pour la génération de PDF)

## ⚙️ Installation

1. Cloner le dépôt :
```bash
git clone [url-du-repo]
cd chatbot_business_plan
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Pour Unix
# ou
venv\\Scripts\\activate   # Pour Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
```
Puis éditer le fichier .env avec vos configurations.

5. Initialiser la base de données :
```bash
python scripts/create_admin.py
```

## 🔧 Configuration

### Variables d'environnement requises :

```env
# Clés secrètes
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key

# Base de données
DATABASE_URL=sqlite:///database/app.db

# Configuration Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Configuration Twilio (WhatsApp)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_whatsapp_number
```

### Configuration des Webhooks

#### Telegram :
```bash
curl "https://api.telegram.org/bot[TELEGRAM_BOT_TOKEN]/setWebhook?url=https://votre-domaine.com/webhook/telegram"
```

#### WhatsApp (Twilio) :
Configurez l'URL du webhook dans votre console Twilio :
```
https://votre-domaine.com/webhook/whatsapp
```

## 🚀 Démarrage

1. Démarrer l'application :
```bash
python src/main.py
```

2. Accéder à l'interface d'administration :
```
http://localhost:5000/
```

Identifiants par défaut :
- Username : admin
- Password : admin123

## 📱 Utilisation

### Commandes du Bot

- `/start` - Démarrer une nouvelle conversation
- `/help` - Afficher l'aide
- `/templates` - Voir les modèles disponibles
- `/cancel` - Annuler l'opération en cours

### Génération d'un Business Plan

1. Démarrer une conversation avec le bot
2. Choisir un template
3. Répondre aux questions du bot
4. Recevoir le business plan généré
5. Exporter dans le format souhaité

## 🛡️ Sécurité

- Authentification JWT pour l'API
- Chiffrement des clés API sensibles
- Validation des webhooks
- Protection CORS
- Gestion des sessions sécurisée

## 📁 Structure du Projet

```
chatbot_business_plan/
├── database/
├── instance/
├── scripts/
│   └── create_admin.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── static/
├── .env
├── .env.example
├── README.md
└── requirements.txt
```

## 🔄 API Routes

### Webhooks
- `POST /webhook/telegram` - Webhook Telegram
- `POST /webhook/whatsapp` - Webhook WhatsApp

### Administration
- `POST /api/admin/login` - Connexion administrateur
- `GET /api/admin/stats` - Statistiques du système

### Business Plans
- `POST /api/business-plan/generate` - Générer un business plan
- `GET /api/business-plan/templates` - Liste des templates
- `POST /api/business-plan/export` - Exporter un business plan

## 📄 Licence

[Type de licence] - voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir `CONTRIBUTING.md` pour plus de détails.

## 📞 Support

Pour toute question ou support :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de développement

## ✨ Remerciements

- Flask et son écosystème
- Twilio pour l'API WhatsApp
- Telegram pour leur API Bot
- WeasyPrint pour la génération de PDF
