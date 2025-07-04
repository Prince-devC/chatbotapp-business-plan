#!/bin/bash

echo "🚀 Déploiement du Chatbot Business Plan..."

# Vérifier que Railway CLI est installé
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI n'est pas installé. Installation..."
    npm install -g @railway/cli
fi

# Se connecter si nécessaire
echo "🔑 Connexion à Railway..."
railway login

# Initialiser le projet si nécessaire
if [ ! -f "railway.json" ]; then
    echo "🏗️ Initialisation du projet Railway..."
    railway init
fi

# Déployer
echo "📦 Déploiement en cours..."
railway up

echo "✅ Déploiement terminé!"
echo "🌐 Votre application sera disponible à l'URL fournie par Railway"

# Afficher les logs
echo "📋 Logs du déploiement:"
railway logs 