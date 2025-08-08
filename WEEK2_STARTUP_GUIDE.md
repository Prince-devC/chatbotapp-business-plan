# 🚀 Guide de Démarrage - Semaine 2 AgroBizChat v2.0

## 📋 Vue d'ensemble

**Objectif :** Intégrer la météo dans le flow et créer un PDF business plan enrichi avec conseils météo et plan d'action temporel.

---

## ✅ Services Créés Semaine 2

### 🛠️ Services Fonctionnels
1. **WeatherService amélioré** - API météo MeteoBenin.bj avec données de test
2. **EnhancedPDFGenerator** - PDF enrichi avec météo et plan d'action
3. **Intégration routes** - Nouvelles routes pour météo et PDF enrichi

### 📊 Fonctionnalités
- ✅ Données météo réalistes par zone agro-écologique
- ✅ Conseils agro-météo spécifiques au maïs
- ✅ PDF avec page de garde, sommaire, météo, plan d'action
- ✅ Plan d'action 30/60/90 jours selon la saison
- ✅ Design moderne avec couleurs agricoles

---

## 🚀 Étapes de Démarrage

### 1. Tests des Services Semaine 2

```bash
# Valider tous les nouveaux services
python test_week2_services.py
```

**Résultat attendu :**
```
🚀 Début des tests Semaine 2 - API Météo & PDF enrichi...

🌦️ Test WeatherService amélioré...
✅ Météo Zone côtière: 28.5°C, 78.2%
✅ Météo Zone des terres de barre: 26.8°C, 72.1%
✅ Météo Zone des collines: 24.3°C, 68.5%
✅ Météo Zone de l'Atacora: 22.1°C, 65.3%
✅ Météo Zone de la Donga: 23.7°C, 69.8%
✅ Prévisions: 7 jours
✅ Conseils agro-météo: 3 conseils
🎉 WeatherService amélioré: Tous les tests passent!

📄 Test EnhancedPDFGenerator...
✅ PDF généré: test_business_plan_enhanced.pdf (15420 bytes)
✅ Plans d'action: 30j(4), 60j(4), 90j(4)
✅ Fichier de test nettoyé
🎉 EnhancedPDFGenerator: Tous les tests passent!

🔗 Test intégration météo + PDF...
✅ PDF d'intégration généré: test_integration_weather.pdf (18250 bytes)
✅ Intégration météo + PDF réussie!

🗺️ Test mapping zones agro-écologiques...
✅ Zone Zone côtière: Cotonou (6.369, 2.4225)
✅ Zone Zone des terres de barre: Abomey-Calavi (6.4969, 2.6043)
✅ Zone Zone des collines: Abomey (7.1761, 1.9911)
✅ Zone Zone de l'Atacora: Natitingou (10.3049, 1.375)
✅ Zone Zone de la Donga: Djougou (9.7, 1.6667)
✅ Zone Zone de l'Ouémé: Porto-Novo (6.6333, 2.4667)
✅ Zone Zone de l'Alibori: Kandi (11.3, 2.35)
✅ Zone Zone du Borgou: Parakou (9.7, 2.6)
✅ Zone Zone du Mono: Lokossa (6.5, 1.75)
✅ Zone Zone du Couffo: Aplahoué (6.85, 1.95)
🎉 Mapping zones: Tous les tests passent!

📊 Résultats des tests Semaine 2:
✅ Tests réussis: 4/4
❌ Tests échoués: 0/4
🎉 Tous les tests passent! Services Semaine 2 prêts pour la production.
```

### 2. Test Manuel des Services

#### Test WeatherService

```python
from src.services.weather_service import WeatherService

# Créer le service
weather_service = WeatherService(use_sandbox=True)

# Test météo actuelle
weather = weather_service.get_current_weather("Zone des terres de barre")
print(f"Température: {weather['temperature']}°C")
print(f"Humidité: {weather['humidity']}%")
print(f"Description: {weather['description']}")

# Test conseils agro-météo
advice = weather_service.get_agro_advice("Zone des terres de barre", "mais")
print(f"Conseils: {advice['conseils']}")
print(f"Actions immédiates: {advice['actions_immediates']}")
```

#### Test EnhancedPDFGenerator

```python
from src.services.enhanced_pdf_generator import EnhancedPDFGenerator

# Créer le générateur
pdf_generator = EnhancedPDFGenerator()

# Données de test
user_data = {
    'username': 'Agriculteur Test',
    'first_name': 'Jean',
    'last_name': 'Dupont',
    'user_type': 'individuel',
    'zone_agro_ecologique': 'Zone des terres de barre',
    'land_area': 2.5,
    'land_unit': 'ha',
    'primary_culture': 'mais'
}

weather_data = {
    'conditions_actuelles': {
        'temperature': '28°C',
        'humidity': '75%',
        'precipitation': '5mm'
    },
    'conseils': ['Température favorable pour la croissance'],
    'actions_immediates': ['Continuer les soins culturaux']
}

# Générer le PDF
pdf_path = pdf_generator.generate_business_plan_pdf(
    user_data=user_data,
    weather_data=weather_data,
    output_path="test_manual.pdf"
)

print(f"PDF généré: {pdf_path}")
```

### 3. Test des Nouvelles Routes

#### Test route météo

```bash
# Test récupération météo
curl -X GET "http://localhost:5000/api/business-plan/weather/Zone%20des%20terres%20de%20barre"
```

**Résultat attendu :**
```json
{
  "current_weather": {
    "temperature": 26.8,
    "humidity": 72.1,
    "precipitation": 3.2,
    "description": "Ensoleillé avec quelques nuages",
    "zone": "Zone des terres de barre"
  },
  "forecast": [...],
  "agro_advice": {
    "culture": "mais",
    "conseils": [...],
    "actions_immediates": [...]
  }
}
```

#### Test route plan d'action

```bash
# Test génération plan d'action
curl -X GET "http://localhost:5000/api/business-plan/action-plan/1"
```

**Résultat attendu :**
```json
{
  "user_info": {
    "name": "Jean Dupont",
    "zone": "Zone des terres de barre",
    "culture": "mais",
    "surface": "2.5 ha"
  },
  "weather_data": {...},
  "action_plan": {
    "30_days": ["Préparation du sol", "Achat des semences", ...],
    "60_days": ["Semis en ligne", "Premier désherbage", ...],
    "90_days": ["Fertilisation de couverture", "Lutte contre les ravageurs", ...]
  }
}
```

---

## 📁 Structure Créée Semaine 2

```
src/services/
├── weather_service.py          # ✅ Amélioré avec données de test
├── enhanced_pdf_generator.py   # ✅ Nouveau - PDF enrichi
└── unit_converter.py          # ✅ Déjà créé semaine 1

src/routes/
└── business_plan.py           # ✅ Nouvelles routes ajoutées

test_week2_services.py         # ✅ Tests complets semaine 2
```

---

## 🎯 Fonctionnalités Validées

### ✅ WeatherService
- [x] Données météo réalistes par zone
- [x] Prévisions 7 jours
- [x] Conseils agro-météo spécifiques
- [x] Actions immédiates et planification
- [x] Mode développement avec données de test

### ✅ EnhancedPDFGenerator
- [x] Page de garde stylisée
- [x] Sommaire automatique
- [x] Section météo intégrée
- [x] Plan d'action 30/60/90 jours
- [x] Analyse économique
- [x] Conseils techniques
- [x] Design moderne agricole

### ✅ Intégration Routes
- [x] Route `/generate-enhanced` pour PDF enrichi
- [x] Route `/weather/<zone>` pour données météo
- [x] Route `/action-plan/<user_id>` pour plan d'action
- [x] Intégration avec base de données

---

## 🚨 Dépannage

### Erreur Import EnhancedPDFGenerator

```bash
# Vérifier l'installation de reportlab
pip install reportlab

# Vérifier l'import
python -c "from src.services.enhanced_pdf_generator import EnhancedPDFGenerator; print('OK')"
```

### Erreur Génération PDF

```bash
# Vérifier les permissions d'écriture
mkdir -p generated_business_plans
chmod 755 generated_business_plans

# Test simple
python -c "
from src.services.enhanced_pdf_generator import EnhancedPDFGenerator
pdf_gen = EnhancedPDFGenerator()
print('PDF Generator OK')
"
```

### Erreur WeatherService

```bash
# Vérifier les imports
python -c "from src.services.weather_service import WeatherService; print('WeatherService OK')"

# Test mode développement
python -c "
from src.services.weather_service import WeatherService
ws = WeatherService(use_sandbox=True)
weather = ws.get_current_weather('Zone des terres de barre')
print(f'Weather OK: {weather[\"temperature\"]}°C')
"
```

---

## 📊 Métriques de Succès Semaine 2

- ✅ **WeatherService** : 10/10 zones agro-écologiques mappées
- ✅ **EnhancedPDFGenerator** : PDF généré avec toutes les sections
- ✅ **Intégration** : Routes fonctionnelles avec base de données
- ✅ **Tests** : 4/4 tests passent

---

## 🎉 Validation Semaine 2

Si vous obtenez :
- ✅ 4/4 tests passent
- ✅ PDF enrichi généré avec météo et plan d'action
- ✅ Routes météo et plan d'action fonctionnelles
- ✅ Données météo réalistes pour toutes les zones

**Alors la Semaine 2 est validée !** 🎉

Vous pouvez passer à la **Semaine 3 - Diagnostic par photo**.

---

## 🔄 Prochaines Étapes

### Semaine 3 - Diagnostic par photo
1. **Réception photos** via WhatsApp/Telegram
2. **Appel API PlantVillage** pour diagnostic
3. **Génération PDF diagnostic** (premium)
4. **Base de données maladies** complète

### Configuration Requise Semaine 3
```env
# API Diagnostic (optionnel pour les tests)
PLANTVILLAGE_API_KEY=your_api_key
``` 