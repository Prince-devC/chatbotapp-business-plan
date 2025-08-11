#!/bin/bash

# Script de déploiement pour Heroku
# Usage: ./deploy_heroku.sh

echo "🚀 Déploiement sur Heroku..."

# Vérifier que Heroku CLI est installé
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI n'est pas installé"
    echo "Installez-le depuis: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Vérifier que l'utilisateur est connecté
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Connexion à Heroku..."
    heroku login
fi

# Demander le nom de l'app
echo "📝 Entrez le nom de votre app Heroku (ou appuyez sur Entrée pour générer automatiquement):"
read -r app_name

if [ -z "$app_name" ]; then
    app_name="agrobiz-chatbot-$(date +%s)"
fi

echo "🏗️  Création de l'app Heroku: $app_name"

# Créer l'app si elle n'existe pas
if ! heroku apps:info "$app_name" &> /dev/null; then
    heroku create "$app_name"
else
    echo "✅ L'app $app_name existe déjà"
fi

# Configurer les variables d'environnement
echo "🔧 Configuration des variables d'environnement..."

# Demander les clés API
echo "🔑 Entrez votre clé API Gemini:"
read -r gemini_key

echo "📱 Entrez votre SID Twilio:"
read -r twilio_sid

echo "🔐 Entrez votre token Twilio:"
read -r twilio_token

echo "📞 Entrez votre numéro WhatsApp Twilio:"
read -r twilio_phone

echo "🤖 Entrez votre token Telegram (optionnel, appuyez sur Entrée pour ignorer):"
read -r telegram_token

# Configurer les variables
heroku config:set FLASK_ENV=production --app "$app_name"
heroku config:set GEMINI_API_KEY="$gemini_key" --app "$app_name"
heroku config:set TWILIO_ACCOUNT_SID="$twilio_sid" --app "$app_name"
heroku config:set TWILIO_AUTH_TOKEN="$twilio_token" --app "$app_name"
heroku config:set TWILIO_PHONE_NUMBER="$twilio_phone" --app "$app_name"

if [ -n "$telegram_token" ]; then
    heroku config:set TELEGRAM_BOT_TOKEN="$telegram_token" --app "$app_name"
fi

# Ajouter l'addon PostgreSQL
echo "🗄️  Ajout de PostgreSQL..."
heroku addons:create heroku-postgresql:mini --app "$app_name"

# Déployer
echo "📤 Déploiement..."
git push heroku main

# Ouvrir l'app
echo "🌐 Ouverture de l'app..."
heroku open --app "$app_name"

echo "✅ Déploiement terminé!"
echo "🌐 Votre app est accessible sur: https://$app_name.herokuapp.com"
echo ""
echo "📊 Pour voir les logs: heroku logs --tail --app $app_name"
echo "🔧 Pour configurer: heroku config --app $app_name" 