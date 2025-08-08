# 🗓️ Plan d'Implémentation AgroBizChat v2.0

## 📋 Vue d'ensemble

**Durée totale :** 8 semaines  
**Objectif final :** Version 2.0 stable avec IA conversationnelle, 2 filières, freemium et diagnostic maladie

---

## ✅ Semaine 1 – Fondations avancées (v1.1)

### 🎯 Objectif
Enrichir le profil utilisateur + début modularité par culture

### 📋 Tâches

#### 🔹 Mise à jour du modèle utilisateur
- [x] Ajout des champs profil agricole (genre, zone, objectif, unité, expérience)
- [x] Support type utilisateur (individuel/coopérative)
- [x] Champs coopératives (nom, membres, commune)

#### 🔹 Collecte complète des données
- [ ] Formulaire de collecte enrichi dans le chatbot
- [ ] Validation des données utilisateur
- [ ] Stockage en base de données

#### 🔹 Conversion automatique des unités
- [x] Service UnitConverter créé
- [ ] Intégration dans le flow de collecte
- [ ] Affichage standardisé (ha/m²)

#### 🔹 Structure modulaire par culture
- [ ] Création dossier `cultures/mais/`
- [ ] Templates spécifiques maïs
- [ ] Séparation des données par culture

### 📤 Livrables
- [x] Modèle User enrichi avec champs agricoles
- [x] Service de conversion d'unités
- [ ] Templates modulaires par culture
- [ ] Formulaire de collecte enrichi

---

## ✅ Semaine 2 – API Météo & génération plan enrichi (v1.2)

### 🎯 Objectif
Intégrer la météo dans le flow

### 📋 Tâches

#### 🔗 Connexion API MeteoBenin.bj
- [x] Service WeatherService créé
- [ ] Configuration API réelle
- [ ] Gestion des erreurs et fallback

#### 📍 Association zone agro-écologique
- [ ] Mapping zones Bénin
- [ ] Attribution automatique selon localisation
- [ ] Validation des coordonnées

#### ☁️ Bloc "Conseil météo" dynamique
- [ ] Intégration dans génération PDF
- [ ] Conseils spécifiques par culture
- [ ] Prévisions 7 jours

#### 🧾 Refonte PDF complet
- [ ] Page de garde stylisée
- [ ] Sommaire automatique
- [ ] Conseils météo intégrés
- [ ] Plan d'action 30/60/90 jours

### 📤 Livrables
- [x] Service météo fonctionnel
- [ ] PDF complet stylisé
- [ ] Conseils météo intégrés
- [ ] Plan d'action temporel

---

## ✅ Semaine 3 – Diagnostic par photo (v1.3)

### 🎯 Objectif
Permettre la détection de maladies par image

### 📋 Tâches

#### 📤 Réception photo WhatsApp/Telegram
- [x] Service DiseaseDetectionService créé
- [ ] Intégration dans webhooks
- [ ] Validation des formats d'image

#### 🔍 Appel modèle IA externe
- [ ] Configuration PlantVillage API
- [ ] Fallback modèle local si nécessaire
- [ ] Gestion des timeouts

#### 📋 Réponse textuelle + fiche traitement
- [ ] Base de données maladies maïs
- [ ] Génération fiches traitement
- [ ] Conseils de prévention

#### 🧾 Génération PDF diagnostic (premium)
- [ ] Template PDF diagnostic
- [ ] Intégration photos
- [ ] Plan de traitement détaillé

### 📤 Livrables
- [x] Service de diagnostic créé
- [ ] Diagnostic complet maïs
- [ ] PDF diagnostic premium
- [ ] Base de données maladies

---

## ✅ Semaine 4 – Conseils post-récolte & transformation (v1.4)

### 🎯 Objectif
Valoriser le produit après la production

### 📋 Tâches

#### 🧃 Fiches transformation
- [ ] Jus d'ananas (recettes, conservation)
- [ ] Amidon de maïs (extraction, utilisation)
- [ ] Emballage (matériaux, techniques)

#### 📦 Conseils circuits de vente
- [ ] Coopératives locales
- [ ] Marchés traditionnels
- [ ] Circuits modernes

#### 📊 Bloc "Plan de valorisation"
- [ ] Intégration dans business plan
- [ ] Calculs de rentabilité
- [ ] Stratégies de commercialisation

#### 📁 Suggestions transformation PDF
- [ ] Section transformation
- [ ] Recettes et techniques
- [ ] Contacts fournisseurs

### 📤 Livrables
- [ ] PDF enrichi transformation
- [ ] Contenu transformation maïs
- [ ] Conseils commercialisation
- [ ] Base de données recettes

---

## ✅ Semaine 5 – Ajout filière Ananas (v1.5)

### 🎯 Objectif
Ajouter une seconde culture complète

### 📋 Tâches

#### 📁 Structure cultures/ananas/
- [ ] Création dossier ananas
- [ ] Templates spécifiques
- [ ] Données techniques

#### 📝 Template Ananas complet
- [ ] Itinéraire technique
- [ ] Analyse économique
- [ ] Fournisseurs spécialisés

#### 🦠 Maladies Ananas + diagnostic
- [ ] Base de données maladies
- [ ] Diagnostic par photo
- [ ] Traitements spécifiques

#### 📄 Génération plans Ananas
- [ ] PDF spécifiques ananas
- [ ] Excel financier
- [ ] Conseils météo adaptés

### 📤 Livrables
- [ ] Génération plan ananas
- [ ] Diagnostic ananas
- [ ] Templates complets
- [ ] Base de données ananas

---

## ✅ Semaine 6 – Paiement & freemium en FCFA (v1.6)

### 🎯 Objectif
Mettre en place la monétisation locale

### 📋 Tâches

#### 💳 Intégration Kkiapay/PayDunya
- [x] Service PaymentService créé
- [ ] Configuration sandbox
- [ ] Tests en production

#### 🔐 Webhooks déblocage automatique
- [ ] Traitement webhooks
- [ ] Déblocage fonctionnalités
- [ ] Gestion des erreurs

#### 🧾 Gestion crédits et paiements
- [ ] Système de crédits
- [ ] Historique paiements
- [ ] Gestion des abonnements

#### 💬 Messages WhatsApp paiement
- [ ] Intégration dans chatbot
- [ ] Messages de paiement
- [ ] Suivi des transactions

### 📤 Livrables
- [x] Service de paiement
- [ ] Packs actifs fonctionnels
- [ ] Paiements FCFA
- [ ] Déblocage automatique

---

## ✅ Semaine 7 – Mode coopérative & rapport groupé (v1.7)

### 🎯 Objectif
Permettre la gestion de projets collectifs

### 📋 Tâches

#### 📥 Formulaire Coopérative
- [ ] Champs spécifiques coopératives
- [ ] Validation données groupées
- [ ] Gestion des membres

#### 📄 Plan collectif PDF
- [ ] Template coopératif
- [ ] Budget groupé
- [ ] Répartition des tâches

#### 📊 Dashboard multi-projets
- [ ] Plans individuels/groupés
- [ ] Statistiques coopératives
- [ ] Suivi des membres

#### 🛒 Fournisseurs volume
- [ ] Fournisseurs gros volumes
- [ ] Négociations groupées
- [ ] Logistique collective

### 📤 Livrables
- [ ] PDF coopératif
- [ ] Administration multi-projets
- [ ] Fournisseurs adaptés
- [ ] Dashboard collectif

---

## ✅ Semaine 8 – Intelligence conversationnelle (v2.0)

### 🎯 Objectif
Répondre à des questions ouvertes

### 📋 Tâches

#### 🧠 Modèle IA local
- [x] Service ConversationalAI créé
- [ ] Entraînement FAQ + scénarios
- [ ] Templates conversationnels

#### ⚙️ Détection d'intention
- [x] Patterns d'intention
- [ ] Classification des questions
- [ ] Confiance des réponses

#### 📚 Corpus FAO/CARDER/ITA
- [ ] Intégration fiches techniques
- [ ] Base de connaissances
- [ ] Mise à jour continue

#### 🔁 Intégration WhatsApp
- [ ] Réponse naturelle
- [ ] Redirection vers fonction
- [ ] Conversation fluide

### 📤 Livrables
- [x] Service IA conversationnelle
- [ ] IA intégrée WhatsApp
- [ ] Corpus technique
- [ ] Réponses naturelles

---

## 🛠️ Services Créés

### ✅ Services Fonctionnels
1. **UnitConverter** - Conversion d'unités agricoles
2. **WeatherService** - API météo MeteoBenin.bj
3. **DiseaseDetectionService** - Diagnostic maladies par photo
4. **PaymentService** - Paiements Kkiapay/PayDunya
5. **ConversationalAI** - IA conversationnelle

### 📋 Modèles Base de Données
- [x] User enrichi (profil agricole, coopératives)
- [ ] WeatherData (données météo)
- [ ] DiseaseDiagnosis (diagnostics maladies)
- [ ] Payment (transactions)
- [ ] Conversation (historique IA)

---

## 🚀 Prochaines Étapes

### Semaine 1 - Priorités
1. **Migration base de données** - Appliquer les nouveaux champs User
2. **Intégration UnitConverter** - Dans le flow de collecte
3. **Templates modulaires** - Créer structure cultures/maïs/
4. **Tests unitaires** - Valider les nouveaux services

### Configuration Requise
```env
# API Météo
METEOBENIN_API_KEY=your_api_key

# Paiements
KKIAPAY_API_KEY=your_api_key
KKIAPAY_SECRET_KEY=your_secret_key
PAYDUNYA_API_KEY=your_api_key
PAYDUNYA_SECRET_KEY=your_secret_key

# IA Diagnostic
PLANTVILLAGE_API_KEY=your_api_key
```

### 📊 Métriques de Succès
- **Semaine 1** : 100% des nouveaux champs collectés
- **Semaine 2** : 90% de précision météo
- **Semaine 3** : 80% de précision diagnostic
- **Semaine 6** : 95% de taux de paiement réussi
- **Semaine 8** : 85% de satisfaction conversationnelle

---

## 🎯 Objectifs Business

### 📈 KPIs Cibles
- **Utilisateurs actifs** : +200% (v1.0 → v2.0)
- **Taux de conversion** : 15% (freemium → premium)
- **Revenus mensuels** : 500 000 FCFA
- **Satisfaction utilisateur** : 4.5/5

### 🎯 Marché Cible
- **Agriculteurs individuels** : 70%
- **Coopératives** : 20%
- **Experts agricoles** : 10%

### 💰 Modèle Freemium
- **Gratuit** : Business plan basique
- **Premium (500 FCFA)** : PDF + Excel + Diagnostic
- **Coopérative (3000 FCFA)** : Plans collectifs + Support prioritaire 