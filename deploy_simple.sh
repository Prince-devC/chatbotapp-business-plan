#!/bin/bash

echo "🚀 Déploiement simplifié AgroBizChat v2.0 sur Railway..."

# Vérifier Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI non installé"
    exit 1
fi

# Vérifier la connexion
if ! railway status &> /dev/null; then
    echo "❌ Non connecté à Railway"
    echo "Exécutez: railway login"
    exit 1
fi

echo "✅ Connecté à Railway"

# Vérifier les fichiers essentiels
required_files=("requirements.txt" "railway.json" "runtime.txt" "Procfile" "src/main.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Fichier manquant: $file"
        exit 1
    fi
    echo "✅ $file"
done

# Déployer
echo "📦 Déploiement en cours..."
if railway up; then
    echo "✅ Déploiement réussi!"
    
    # Attendre et vérifier
    echo "⏳ Attente du démarrage..."
    sleep 30
    
    # Récupérer l'URL
    echo "🔗 Récupération de l'URL..."
    APP_URL=$(railway status --json 2>/dev/null | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$APP_URL" ]; then
        echo "🌐 Application déployée sur: $APP_URL"
        echo ""
        echo "🎉 AgroBizChat v2.0 déployé avec succès!"
        echo ""
        echo "📊 Fonctionnalités déployées:"
        echo "✅ Support multilingue (Français, Fon, Yoruba, Mina, Bariba)"
        echo "✅ Optimisations performance (Cache Redis, Monitoring)"
        echo "✅ Support ananas complet"
        echo "✅ Système de paiement local (FCFA)"
        echo "✅ Diagnostic maladies par photo"
        echo "✅ IA conversationnelle avancée"
        echo "✅ Business plans spécialisés"
        echo ""
        echo "🔗 URLs importantes:"
        echo "📱 Application: $APP_URL"
        echo "🌍 API localisation: $APP_URL/api/localization"
        echo "⚡ API performance: $APP_URL/api/performance"
        echo "🍍 API ananas: $APP_URL/api/business-plan/pineapple"
        echo "💳 API paiements: $APP_URL/api/payment"
    else
        echo "⚠️ URL non récupérée"
    fi
else
    echo "❌ Déploiement échoué"
    exit 1
fi 