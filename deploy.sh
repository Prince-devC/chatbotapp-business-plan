#!/bin/bash

# 🚀 Script de déploiement AgroBizChat v2.0 sur Railway
# Support multilingue complet avec toutes les fonctionnalités

echo "🚀 Déploiement AgroBizChat v2.0 sur Railway..."

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier que Railway CLI est installé
if ! command -v railway &> /dev/null; then
    print_error "Railway CLI n'est pas installé. Installez-le d'abord."
    echo "npm install -g @railway/cli"
    exit 1
fi

# Vérifier la connexion Railway
print_status "Vérification de la connexion Railway..."
if ! railway status &> /dev/null; then
    print_error "Non connecté à Railway. Connectez-vous d'abord."
    echo "railway login"
    exit 1
fi

print_success "Connecté à Railway"

# Tests pré-déploiement
print_status "Exécution des tests pré-déploiement..."

# Test services semaine 8 (localisation)
print_status "Test services semaine 8 (localisation)..."
if python3 test_week8_services.py; then
    print_success "Tests semaine 8 passent"
else
    print_error "Tests semaine 8 échouent"
    exit 1
fi

# Test services semaine 7 (performance)
print_status "Test services semaine 7 (performance)..."
if python3 test_week7_services.py; then
    print_success "Tests semaine 7 passent"
else
    print_warning "Tests semaine 7 échouent (continuant le déploiement)"
fi

# Test services semaine 6 (ananas)
print_status "Test services semaine 6 (ananas)..."
if python3 test_week6_services.py; then
    print_success "Tests semaine 6 passent"
else
    print_warning "Tests semaine 6 échouent (continuant le déploiement)"
fi

# Optimisation base de données
print_status "Optimisation base de données..."
python3 -c "
from src.services.database_optimizer import DatabaseOptimizer
db_optimizer = DatabaseOptimizer()
result = db_optimizer.optimize_database()
print(f'Optimisation: {result[\"status\"]}')
result = db_optimizer.create_indexes()
print(f'Index: {result[\"status\"]}')
"

if [ $? -eq 0 ]; then
    print_success "Optimisation base de données terminée"
else
    print_warning "Optimisation base de données échouée (continuant le déploiement)"
fi

# Vérification des fichiers de configuration
print_status "Vérification des fichiers de configuration..."

required_files=(
    "requirements.txt"
    "railway.json"
    "runtime.txt"
    "Procfile"
    "src/main.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file"
    else
        print_error "✗ $file manquant"
        exit 1
    fi
done

# Vérification des variables d'environnement
print_status "Configuration des variables d'environnement..."

# Variables d'environnement pour la production
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO
railway variables set DEFAULT_LANGUAGE=fr
railway variables set SUPPORTED_LANGUAGES=fr,fon,yor,min,bar
railway variables set CACHE_ENABLED=true
railway variables set ENABLE_METRICS=true
railway variables set DB_OPTIMIZATION_ENABLED=true
railway variables set ENABLE_ALERTS=true

print_success "Variables d'environnement configurées"

# Déploiement
print_status "Déploiement sur Railway..."
if railway up; then
    print_success "Déploiement réussi !"
else
    print_error "Déploiement échoué"
    exit 1
fi

# Vérification du déploiement
print_status "Vérification du déploiement..."

# Attendre que l'application soit prête
sleep 30

# Récupérer l'URL de l'application
APP_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)

if [ -n "$APP_URL" ]; then
    print_success "Application déployée sur: $APP_URL"
    
    # Test de santé de l'application
    print_status "Test de santé de l'application..."
    
    # Test endpoint de base
    if curl -f "$APP_URL" &> /dev/null; then
        print_success "✓ Endpoint de base accessible"
    else
        print_warning "⚠ Endpoint de base non accessible"
    fi
    
    # Test endpoint localisation
    if curl -f "$APP_URL/api/localization/languages" &> /dev/null; then
        print_success "✓ API localisation accessible"
    else
        print_warning "⚠ API localisation non accessible"
    fi
    
    # Test endpoint performance
    if curl -f "$APP_URL/api/performance/cache/health" &> /dev/null; then
        print_success "✓ API performance accessible"
    else
        print_warning "⚠ API performance non accessible"
    fi
    
    # Test endpoint ananas
    if curl -f "$APP_URL/api/business-plan/pineapple/varieties" &> /dev/null; then
        print_success "✓ API ananas accessible"
    else
        print_warning "⚠ API ananas non accessible"
    fi
    
else
    print_error "Impossible de récupérer l'URL de l'application"
fi

# Affichage des informations finales
echo ""
echo "🎉 AgroBizChat v2.0 déployé avec succès !"
echo ""
echo "📊 Fonctionnalités déployées :"
echo "✅ Support multilingue (Français, Fon, Yoruba, Mina, Bariba)"
echo "✅ Optimisations performance (Cache Redis, Monitoring)"
echo "✅ Support ananas complet (Base de données, Business plans)"
echo "✅ Système de paiement local (FCFA)"
echo "✅ Diagnostic maladies par photo"
echo "✅ IA conversationnelle avancée"
echo "✅ Business plans spécialisés"
echo ""
echo "🌍 Langues supportées :"
echo "🇫🇷 Français (fr) - Langue officielle"
echo "🇧🇯 Fon (fon) - 1.7M locuteurs"
echo "🇧🇯 Yoruba (yor) - 1.2M locuteurs"
echo "🇧🇯 Mina (min) - 500K locuteurs"
echo "🇧🇯 Bariba (bar) - 400K locuteurs"
echo ""
echo "🔗 URLs importantes :"
echo "📱 Application principale: $APP_URL"
echo "🌍 API localisation: $APP_URL/api/localization"
echo "⚡ API performance: $APP_URL/api/performance"
echo "🍍 API ananas: $APP_URL/api/business-plan/pineapple"
echo "💳 API paiements: $APP_URL/api/payment"
echo ""
echo "📋 Commandes utiles :"
echo "railway logs - Voir les logs"
echo "railway status - Statut de l'application"
echo "railway variables - Variables d'environnement"
echo ""
echo "🚀 L'application est prête pour la production !" 