#!/bin/bash

# Script de déploiement principal - Choix de plateforme
# Usage: ./deploy.sh

echo "🚀 Déploiement AgroBiz Chatbot"
echo "================================"
echo ""

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

# Menu de sélection de plateforme
echo "🌐 Choisissez votre plateforme de déploiement:"
echo ""
echo "1. 🎯 Render (RECOMMANDÉ - Gratuit, Simple)"
echo "2. 🚀 Heroku (Gratuit, Populaire)"
echo "3. ⚡ Vercel (Gratuit, Rapide)"
echo "4. 📋 Voir le guide complet"
echo "5. ❌ Annuler"
echo ""

read -p "Votre choix (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🎯 Déploiement sur Render..."
        echo "Suivez ces étapes:"
        echo ""
        echo "1. Allez sur https://render.com"
        echo "2. Connectez votre compte GitHub"
        echo "3. Cliquez 'New +' → 'Web Service'"
        echo "4. Sélectionnez votre repository"
        echo "5. Render détectera automatiquement le render.yaml"
        echo "6. Configurez vos variables d'environnement"
        echo ""
        echo "🌐 Votre app sera accessible sur: https://agrobiz-chatbot.onrender.com"
        echo ""
        echo "📋 Variables d'environnement à configurer:"
        echo "- GEMINI_API_KEY: Votre clé API Gemini"
        echo "- TWILIO_ACCOUNT_SID: Votre SID Twilio"
        echo "- TWILIO_AUTH_TOKEN: Votre token Twilio"
        echo "- TWILIO_PHONE_NUMBER: Votre numéro WhatsApp"
        echo "- TELEGRAM_BOT_TOKEN: Votre token Telegram"
        ;;
    2)
        echo ""
        echo "🚀 Déploiement sur Heroku..."
        echo "Lancez le script Heroku:"
        echo "./deploy_heroku.sh"
        ;;
    3)
        echo ""
        echo "⚡ Déploiement sur Vercel..."
        echo "Lancez le script Vercel:"
        echo "./deploy_vercel.sh"
        ;;
    4)
        echo ""
        echo "📋 Guide complet de déploiement:"
        echo "cat DEPLOYMENT_ALTERNATIVES.md"
        echo ""
        echo "Ou ouvrez le fichier DEPLOYMENT_ALTERNATIVES.md dans votre éditeur"
        ;;
    5)
        echo "❌ Déploiement annulé"
        exit 0
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "🎉 Déploiement configuré!"
echo "📚 Consultez DEPLOYMENT_ALTERNATIVES.md pour plus de détails" 