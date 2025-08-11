#!/bin/bash

# Script de déploiement pour Render
# Usage: ./deploy_render.sh

echo "🚀 Déploiement sur Render..."

# Vérifier que git est configuré
if ! git remote -v | grep -q "origin"; then
    echo "❌ Erreur: Pas de remote 'origin' configuré"
    echo "Configurez d'abord votre repository GitHub:"
    echo "git remote add origin https://github.com/votre-username/votre-repo.git"
    exit 1
fi

# Vérifier que tous les changements sont commités
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Attention: Vous avez des changements non commités"
    echo "Voulez-vous les committer maintenant? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        git add .
        echo "Entrez votre message de commit:"
        read -r commit_msg
        git commit -m "$commit_msg"
    else
        echo "❌ Déploiement annulé. Committez d'abord vos changements."
        exit 1
    fi
fi

# Pousser vers GitHub
echo "📤 Pousse vers GitHub..."
git push origin main

echo "✅ Code poussé vers GitHub!"
echo ""
echo "🔗 Allez sur https://render.com pour:"
echo "1. Connecter votre repository GitHub"
echo "2. Créer un nouveau Web Service"
echo "3. Sélectionner votre repo"
echo "4. Render détectera automatiquement le render.yaml"
echo ""
echo "📋 Variables d'environnement à configurer:"
echo "- GEMINI_API_KEY: Votre clé API Gemini"
echo "- TWILIO_ACCOUNT_SID: Votre SID Twilio"
echo "- TWILIO_AUTH_TOKEN: Votre token Twilio"
echo "- TWILIO_PHONE_NUMBER: Votre numéro WhatsApp"
echo "- TELEGRAM_BOT_TOKEN: Votre token Telegram"
echo ""
echo "🌐 Votre app sera accessible sur: https://agrobiz-chatbot.onrender.com" 