# 🚀 Guide de Démarrage - Semaine 1 AgroBizChat v2.0

## 📋 Vue d'ensemble

**Objectif :** Mettre en place les fondations avancées avec profil utilisateur enrichi et modularité par culture.

---

## ✅ Services Créés

### 🛠️ Services Fonctionnels
1. **UnitConverter** - Conversion automatique des unités agricoles
2. **WeatherService** - API météo MeteoBenin.bj  
3. **DiseaseDetectionService** - Diagnostic maladies par photo
4. **PaymentService** - Paiements Kkiapay/PayDunya
5. **ConversationalAI** - IA conversationnelle

### 📊 Modèle User Enrichi
- ✅ Champs profil agricole (genre, zone, objectif, unité, expérience)
- ✅ Support type utilisateur (individuel/coopérative)
- ✅ Champs coopératives (nom, membres, commune)

---

## 🚀 Étapes de Démarrage

### 1. Migration Base de Données

```bash
# Exécuter la migration pour ajouter les nouveaux champs
python scripts/migrate_user_model.py
```

**Résultat attendu :**
```
🚀 Début de la migration du modèle User...
Colonnes existantes: ['id', 'platform', 'platform_user_id', ...]
Ajout de la colonne: user_type
✅ Colonne user_type ajoutée avec succès
...
✅ Migration terminée avec succès!
📊 Statistiques:
Total utilisateurs: X
Individuels: X
Coopératives: X
```

### 2. Tests des Services

```bash
# Valider tous les nouveaux services
python test_agrobiz_services.py
```

**Résultat attendu :**
```
🚀 Début des tests AgroBizChat v2.0...

🧪 Test UnitConverter...
✅ Conversion canti->ha OK
✅ Conversion canti->m2 OK
✅ Surface standard OK
✅ Formatage affichage OK
🎉 UnitConverter: Tous les tests passent!

🌦️ Test WeatherService...
✅ Mapping zones OK
🎉 WeatherService: Tests de base passent!

🔍 Test DiseaseDetectionService...
✅ Génération diagnostic OK
✅ Base de données traitements OK
✅ Base de données prévention OK
🎉 DiseaseDetectionService: Tests de base passent!

💳 Test PaymentService...
✅ Packages de prix OK
🎉 PaymentService: Tests de base passent!

🤖 Test ConversationalAI...
✅ Détection d'intention OK
✅ Traitement message FAQ OK
✅ Traitement message technique OK
✅ Traitement message général OK
✅ Base FAQ OK
✅ Patterns d'intention OK
🎉 ConversationalAI: Tous les tests passent!

📊 Résultats des tests:
✅ Tests réussis: 5/5
❌ Tests échoués: 0/5
🎉 Tous les tests passent! Services prêts pour la production.
```

### 3. Configuration Environnement

Ajouter dans votre fichier `.env` :

```env
# API Météo (optionnel pour les tests)
METEOBENIN_API_KEY=your_api_key

# Paiements (optionnel pour les tests)
KKIAPAY_API_KEY=your_api_key
KKIAPAY_SECRET_KEY=your_secret_key
PAYDUNYA_API_KEY=your_api_key
PAYDUNYA_SECRET_KEY=your_secret_key

# IA Diagnostic (optionnel pour les tests)
PLANTVILLAGE_API_KEY=your_api_key
```

### 4. Installation Dépendances

```bash
# Mettre à jour les dépendances
pip install -r requirements.txt
```

---

## 🧪 Tests Manuels

### Test UnitConverter

```python
from src.services.unit_converter import UnitConverter

# Test conversion
ha_value = UnitConverter.convert_area(10, 'canti', 'ha')
print(f"10 canti = {ha_value} ha")  # Devrait afficher: 0.4

# Test surface standard
standard = UnitConverter.get_standard_area(10, 'canti')
print(f"Surface standard: {standard}")  # {'ha': 0.4, 'm2': 4000}

# Test formatage
display = UnitConverter.format_area_display(standard)
print(f"Affichage: {display}")  # "0.4 hectare(s) (4000 m²)"
```

### Test ConversationalAI

```python
from src.services.conversational_ai import ConversationalAI

ai = ConversationalAI()

# Test question FAQ
response = ai.process_message("Comment planter du maïs ?")
print(f"Réponse: {response['response']}")

# Test question technique
response = ai.process_message("Quels engrais utiliser ?")
print(f"Type: {response['intent']['type']}")  # Devrait être 'technical'
```

---

## 📁 Structure Créée

```
src/services/
├── unit_converter.py      # Conversion d'unités agricoles
├── weather_service.py     # API météo MeteoBenin.bj
├── disease_detection.py   # Diagnostic maladies par photo
├── payment_service.py     # Paiements Kkiapay/PayDunya
└── conversational_ai.py   # IA conversationnelle

scripts/
└── migrate_user_model.py  # Migration base de données

test_agrobiz_services.py  # Tests complets
```

---

## 🎯 Prochaines Étapes

### Semaine 1 - Tâches Restantes

1. **Intégration UnitConverter dans le chatbot**
   - Modifier le flow de collecte pour utiliser la conversion automatique
   - Afficher les surfaces en unités standard

2. **Templates modulaires par culture**
   - Créer dossier `cultures/mais/`
   - Séparer les templates par culture
   - Adapter les questions selon la culture

3. **Formulaire de collecte enrichi**
   - Ajouter les nouveaux champs dans le chatbot
   - Validation des données
   - Stockage en base

4. **Tests d'intégration**
   - Tester le flow complet avec les nouveaux champs
   - Valider la conversion d'unités
   - Tester l'IA conversationnelle

---

## 🚨 Dépannage

### Erreur Migration Base de Données

```bash
# Si erreur de migration
rm database/app.db
python scripts/create_admin.py
python scripts/migrate_user_model.py
```

### Erreur Tests

```bash
# Vérifier les imports
python -c "from src.services.unit_converter import UnitConverter; print('OK')"

# Vérifier la base de données
python -c "from src.main import app, db; print('DB OK')"
```

### Erreur Dépendances

```bash
# Réinstaller les dépendances
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

---

## 📊 Métriques de Succès

- ✅ **Migration DB** : 100% des nouveaux champs ajoutés
- ✅ **Tests UnitConverter** : 100% des conversions correctes
- ✅ **Tests ConversationalAI** : 100% des intentions détectées
- ✅ **Tests de base** : 5/5 services fonctionnels

---

## 🎉 Validation Semaine 1

Si vous obtenez :
- ✅ Migration réussie avec données d'exemple
- ✅ 5/5 tests passent
- ✅ Services importables sans erreur

**Alors la Semaine 1 est validée !** 🎉

Vous pouvez passer à la **Semaine 2 - API Météo & génération plan enrichi**. 