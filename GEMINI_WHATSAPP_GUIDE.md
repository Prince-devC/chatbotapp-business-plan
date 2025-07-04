# Guide d'Utilisation : Système Gemini AI + WhatsApp Business Plan

## 🎯 Vue d'Ensemble

Ce système permet de générer automatiquement des business plans complets via WhatsApp en utilisant l'intelligence artificielle Gemini de Google. 

**Fonctionnalités principales :**
- 📱 Réception de messages WhatsApp avec demandes de business plan
- 🤖 Analyse automatique avec Gemini AI des documents de la base de données
- 📊 Génération d'un Business Plan au format Excel
- 🔧 Génération d'un Itinéraire Technique au format PDF
- 📤 Envoi automatique des fichiers via WhatsApp

## 🚀 Configuration

### 1. Variables d'Environnement (.env)

```bash
# Configuration Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here

# Configuration WhatsApp via Twilio
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your-webhook-verify-token
```

### 2. Obtenir une Clé API Gemini

1. Aller sur [Google AI Studio](https://aistudio.google.com/)
2. Créer un nouveau projet
3. Générer une clé API
4. Ajouter la clé dans votre fichier `.env`

### 3. Configuration Twilio WhatsApp

1. Créer un compte [Twilio](https://www.twilio.com/)
2. Activer WhatsApp Business API
3. Configurer le webhook : `https://votre-domaine.com/webhook/whatsapp-gemini`

## 📋 Utilisation

### WhatsApp Bot

**URL du Webhook :** `/webhook/whatsapp-gemini`

**Fonctionnement :**
1. L'utilisateur envoie un message décrivant son projet d'entreprise
2. Le système analyse tous les templates de la base de données
3. Gemini génère un business plan personnalisé
4. Deux fichiers sont créés et envoyés :
   - 📊 **Business Plan Excel** : Analyse complète avec tableaux financiers
   - 🔧 **Itinéraire Technique PDF** : Spécifications techniques détaillées

### Exemple de Message WhatsApp

```
"Je veux créer une startup de livraison de repas healthy 
ciblant les jeunes actifs urbains avec une app mobile innovante"
```

**Réponse automatique :**
- Message de bienvenue avec confirmation
- Génération des documents (Excel + PDF)  
- Envoi des fichiers avec liens de téléchargement
- Résumé du business plan généré

## 🛠️ API Endpoints

### Test de Génération
```bash
POST /api/chatbot/test-gemini
Content-Type: application/json

{
    "message": "Description de votre projet",
    "phone": "numéro_de_test"
}
```

### Téléchargement des Fichiers
```
GET /download/{filename}
```

## 📁 Structure des Fichiers Générés

### Business Plan Excel (.xlsx)
- **Feuille 1 :** Résumé Exécutif
- **Feuille 2 :** Analyse du Marché  
- **Feuille 3 :** Projections Financières (tableaux détaillés)
- **Feuille 4 :** Stratégie Marketing
- **Feuille 5 :** Plan Opérationnel
- **Feuille 6 :** Risques & Opportunités

### Itinéraire Technique PDF (.pdf)
- **Section 1 :** Architecture Technique
- **Section 2 :** Spécifications Détaillées
- **Section 3 :** Étapes de Développement
- **Section 4 :** Planning d'Implémentation
- **Section 5 :** Ressources Techniques
- **Section 6 :** Technologies Recommandées
- **Section 7 :** Contraintes et Solutions
- **Section 8 :** Recommandations Techniques

## 🔧 Architecture Technique

```
WhatsApp Message → Webhook → Gemini Analysis → Document Generation → WhatsApp Response
```

### Services Principaux

1. **GeminiAnalysisService** (`src/services/gemini_service.py`)
   - Analyse des documents de la base
   - Génération du contenu avec Gemini
   - Extraction de texte multi-format

2. **DocumentGenerator** (`src/services/document_generator.py`)
   - Génération Excel avec formatage professionnel
   - Génération PDF avec mise en page technique
   - Gestion des styles et tableaux

3. **WhatsAppService** (`src/services/whatsapp_service.py`)
   - Envoi de messages via Twilio
   - Gestion des documents joints
   - Messages d'erreur personnalisés

## 📊 Exemple de Workflow Complet

1. **Réception Message WhatsApp**
   ```
   "Créer une plateforme e-commerce B2B pour l'industrie textile"
   ```

2. **Analyse Gemini**
   - Scan de tous les templates uploadés
   - Extraction des informations pertinentes
   - Génération du contenu structuré

3. **Génération des Documents**
   - **Excel :** Business plan avec projections financières
   - **PDF :** Itinéraire technique avec architecture système

4. **Envoi WhatsApp**
   ```
   ✅ Business Plan généré avec succès !
   
   📊 Documents analysés: 15
   📁 Fichiers générés:
   • 📊 Business Plan Excel: business_plan_20241215_143025.xlsx
   • 🔧 Itinéraire Technique PDF: itineraire_technique_20241215_143025.pdf
   
   💾 Téléchargement: https://votre-domaine.com/download/...
   ```

## 🚨 Gestion des Erreurs

### Messages d'Erreur Automatiques

- **Pas de templates :** "Aucun document disponible dans la base"
- **Erreur Gemini :** "Erreur lors de l'analyse IA" 
- **Erreur génération :** "Impossible de créer les fichiers"
- **Erreur système :** "Service temporairement indisponible"

### Conseils pour l'Utilisateur

Le bot envoie automatiquement des conseils si la génération échoue :
- Décrire clairement le secteur d'activité
- Mentionner la cible client
- Préciser la proposition de valeur
- Indiquer le modèle économique

## 📈 Monitoring et Logs

Tous les événements sont loggés avec des emojis pour faciliter le suivi :

```
📱 Message WhatsApp reçu
🤖 Analyse Gemini en cours
📊 Génération Excel terminée
🔧 Génération PDF terminée
✅ Envoi réussi
❌ Erreur détectée
```

## 🔒 Sécurité

- Validation des webhooks Twilio
- Limitation des types de fichiers
- Gestion des timeouts
- Protection contre les attaques par déni de service

## 🎛️ Administration

Les templates peuvent être gérés via l'interface web :
- Upload de nouveaux documents
- Catégorisation
- Prévisualisation
- Activation/désactivation 