#!/bin/bash

# Script de déploiement pour Vercel
# Usage: ./deploy_vercel.sh

echo "🚀 Déploiement sur Vercel..."

# Vérifier que Vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI n'est pas installé"
    echo "Installez-le avec: npm i -g vercel"
    exit 1
fi

# Vérifier que l'utilisateur est connecté
if ! vercel whoami &> /dev/null; then
    echo "🔐 Connexion à Vercel..."
    vercel login
fi

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

# Déployer sur Vercel
echo "🚀 Déploiement sur Vercel..."
vercel --prod

echo "✅ Déploiement terminé!"
echo ""
echo "📋 Variables d'environnement à configurer sur Vercel:"
echo "- GEMINI_API_KEY: Votre clé API Gemini"
echo "- TWILIO_ACCOUNT_SID: Votre SID Twilio"
echo "- TWILIO_AUTH_TOKEN: Votre token Twilio"
echo "- TWILIO_PHONE_NUMBER: Votre numéro WhatsApp"
echo "- TELEGRAM_BOT_TOKEN: Votre token Telegram"
echo ""
echo "🔗 Pour configurer les variables: vercel env add"
echo "📊 Pour voir les logs: vercel logs" 