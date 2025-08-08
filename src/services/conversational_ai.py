"""
Service d'Intelligence Conversationnelle pour AgroBizChat
Détection d'intention, FAQ automatique et réponses contextuelles
"""

import re
import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os

class ConversationalAI:
    """Service d'IA conversationnelle avancée"""
    
    def __init__(self):
        self.intents = self._load_intents()
        self.faq_data = self._load_faq()
        self.scenarios = self._load_scenarios()
        self.context = {}
        
    def _load_intents(self) -> Dict:
        """Charge les patterns d'intention"""
        return {
            'greeting': {
                'patterns': [
                    r'bonjour|salut|hello|hi|bonsoir',
                    r'comment allez-vous|ça va|comment ça va',
                    r'bonne journée|bonne soirée'
                ],
                'responses': [
                    "Bonjour ! Je suis AgroBizChat, votre assistant agricole. Comment puis-je vous aider aujourd'hui ? 🌾",
                    "Salut ! Je suis là pour vous accompagner dans vos projets agricoles. Que souhaitez-vous faire ? 🌱",
                    "Bonjour ! Prêt à optimiser votre exploitation agricole ? Parlez-moi de vos besoins ! 🚜"
                ]
            },
            'business_plan': {
                'patterns': [
                    r'business plan|plan d\'affaires|projet agricole',
                    r'créer un business plan|générer un plan',
                    r'étude de faisabilité|viabilité économique'
                ],
                'responses': [
                    "Je peux vous aider à créer un business plan agricole complet ! 📊\n\nPour commencer, j'ai besoin de quelques informations :\n• Votre zone agro-écologique\n• La culture principale\n• La superficie de votre exploitation\n• Votre objectif (commercial, familial, etc.)\n\nDites-moi ces détails et je générerai un plan personnalisé !",
                    "Excellent choix ! Un business plan bien structuré est essentiel pour réussir. 📈\n\nJe vais vous guider étape par étape. Commençons par votre profil agricole :\n• Zone géographique\n• Culture principale\n• Surface cultivée\n• Expérience agricole\n\nQuelle est votre zone agro-écologique ?"
                ]
            },
            'weather': {
                'patterns': [
                    r'météo|climat|précipitations|température',
                    r'conditions météo|prévisions météo',
                    r'pluie|sécheresse|humidité'
                ],
                'responses': [
                    "Je peux vous fournir des informations météo précises pour votre zone ! 🌦️\n\nPour des conseils agro-météo personnalisés, dites-moi :\n• Votre zone agro-écologique\n• Votre culture principale\n• La période qui vous intéresse\n\nJe vous donnerai alors des conseils adaptés à vos besoins !",
                    "La météo est cruciale pour vos cultures ! 🌤️\n\nJe peux vous aider avec :\n• Les prévisions météo de votre zone\n• Les conseils agro-météo\n• Les alertes climatiques\n• Les recommandations culturales\n\nQuelle est votre zone agro-écologique ?"
                ]
            },
            'disease_diagnosis': {
                'patterns': [
                    r'maladie|maladie des plantes|symptômes',
                    r'feuilles jaunes|taches|pourriture',
                    r'diagnostic|identification maladie'
                ],
                'responses': [
                    "Je peux vous aider à diagnostiquer les maladies de vos plantes ! 🔍\n\nPour un diagnostic précis :\n• Prenez une photo claire de la plante malade\n• Incluez les feuilles, tiges et racines si possible\n• Décrivez les symptômes observés\n\nEnvoyez-moi la photo et je vous donnerai un diagnostic détaillé avec les traitements recommandés !",
                    "Le diagnostic précoce est essentiel ! 🌿\n\nJe peux identifier :\n• Les maladies fongiques\n• Les carences nutritionnelles\n• Les attaques d'insectes\n• Les problèmes physiologiques\n\nEnvoyez-moi une photo de vos plantes malades pour un diagnostic complet !"
                ]
            },
            'payment': {
                'patterns': [
                    r'paiement|tarif|prix|abonnement',
                    r'combien ça coûte|tarification|packages',
                    r'premium|basique|coopérative'
                ],
                'responses': [
                    "Voici nos packages AgroBizChat : 💳\n\n🆓 **Gratuit**\n• Business plans basiques\n• Météo de base\n• Support chat\n\n💳 **Basique (500 FCFA)**\n• Tout du gratuit\n• PDF premium inclus\n\n⭐ **Premium (1500 FCFA)**\n• Tout du basique\n• Diagnostic photo inclus\n\n👥 **Coopérative (3000 FCFA)**\n• Tout du premium\n• Fonctionnalités groupe\n\nQuel package vous intéresse ?",
                    "Nos tarifs sont adaptés aux agriculteurs ! 💰\n\n**Packages disponibles :**\n• Gratuit : Fonctionnalités de base\n• Basique : 500 FCFA/mois\n• Premium : 1500 FCFA/mois\n• Coopérative : 3000 FCFA/mois\n\nChaque niveau débloque de nouvelles fonctionnalités. Voulez-vous en savoir plus sur un package spécifique ?"
                ]
            },
            'help': {
                'patterns': [
                    r'aide|help|comment faire|comment utiliser',
                    r'je ne comprends pas|je suis perdu',
                    r'fonctionnalités|que puis-je faire'
                ],
                'responses': [
                    "Je suis là pour vous aider ! 🤝\n\n**Mes fonctionnalités principales :**\n\n📊 **Business Plans**\n• Création de plans d'affaires agricoles\n• Études de faisabilité\n• Analyses économiques\n\n🌦️ **Météo & Conseils**\n• Prévisions météo par zone\n• Conseils agro-météo\n• Alertes climatiques\n\n🔍 **Diagnostic Photo**\n• Identification des maladies\n• Conseils de traitement\n• Prévention des problèmes\n\n💳 **Packages Premium**\n• Fonctionnalités avancées\n• PDF détaillés\n• Support prioritaire\n\nQue souhaitez-vous explorer ?",
                    "Voici comment je peux vous aider ! 🚀\n\n**Mes services :**\n\n1️⃣ **Business Plans Agricoles**\nDites-moi votre zone et culture, je crée un plan complet\n\n2️⃣ **Conseils Météo**\nPrévisions et conseils adaptés à votre zone\n\n3️⃣ **Diagnostic Maladies**\nEnvoyez une photo, je diagnostique et conseille\n\n4️⃣ **Packages Premium**\nFonctionnalités avancées selon vos besoins\n\nPar quoi voulez-vous commencer ?"
                ]
            },
            'goodbye': {
                'patterns': [
                    r'au revoir|bye|à bientôt|merci',
                    r'fin de conversation|terminer|quitter'
                ],
                'responses': [
                    "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions. Bonne continuation dans vos projets agricoles ! 🌾👋",
                    "Merci de votre confiance ! Je reste disponible pour vous accompagner dans vos projets agricoles. À bientôt ! 🚜👋",
                    "À bientôt ! N'oubliez pas que je suis là pour vous aider à réussir vos projets agricoles. Bonne journée ! 🌱👋"
                ]
            }
        }
    
    def _load_faq(self) -> Dict:
        """Charge la base de connaissances FAQ"""
        return {
            'business_plan': {
                'questions': [
                    'comment créer un business plan',
                    'quelles informations pour un business plan',
                    'business plan agricole',
                    'étude de faisabilité'
                ],
                'answer': """📊 **Création d'un Business Plan Agricole**

**Étapes pour un business plan réussi :**

1️⃣ **Analyse de votre situation**
• Zone agro-écologique
• Culture principale
• Surface disponible
• Expérience agricole

2️⃣ **Étude de marché**
• Demande locale
• Concurrence
• Prix de vente
• Canaux de distribution

3️⃣ **Plan financier**
• Coûts de production
• Revenus attendus
• Rentabilité
• Sources de financement

4️⃣ **Plan opérationnel**
• Calendrier cultural
• Besoins en main d'œuvre
• Équipements nécessaires
• Gestion des risques

**Je peux vous aider à créer un business plan complet ! Dites-moi votre zone et culture principale."""
            },
            'weather_advice': {
                'questions': [
                    'conseils météo',
                    'prévisions météo agricole',
                    'météo pour agriculture',
                    'conseils agro-météo'
                ],
                'answer': """🌦️ **Conseils Agro-Météo**

**Comment optimiser selon la météo :**

🌧️ **En cas de pluie :**
• Évitez les traitements phytosanitaires
• Surveillez les risques de maladies
• Protégez les cultures sensibles

☀️ **En cas de sécheresse :**
• Irriguez aux heures fraîches
• Paillez pour conserver l'humidité
• Surveillez les stress hydriques

🌡️ **Gestion des températures :**
• Semis selon les températures optimales
• Protection contre les gelées
• Ventilation des serres

**Je peux vous donner des conseils personnalisés selon votre zone et culture !"""
            },
            'disease_management': {
                'questions': [
                    'maladies des plantes',
                    'traitement maladies',
                    'prévention maladies',
                    'symptômes plantes'
                ],
                'answer': """🔍 **Gestion des Maladies des Plantes**

**Prévention :**
• Rotation des cultures
• Variétés résistantes
• Hygiène des outils
• Espacement approprié

**Surveillance :**
• Inspection régulière
• Détection précoce
• Identification des symptômes
• Suivi des conditions favorables

**Traitement :**
• Diagnostic précis
• Traitements appropriés
• Respect des doses
• Rotation des produits

**Je peux diagnostiquer vos plantes à partir d'une photo ! Envoyez-moi une image claire."""
            },
            'payment_info': {
                'questions': [
                    'tarifs',
                    'prix services',
                    'abonnements',
                    'packages'
                ],
                'answer': """💳 **Tarification AgroBizChat**

**Nos packages :**

🆓 **Gratuit**
• Business plans basiques
• Météo de base
• Support chat

💳 **Basique (500 FCFA/mois)**
• Tout du gratuit
• PDF premium détaillés
• Conseils personnalisés

⭐ **Premium (1500 FCFA/mois)**
• Tout du basique
• Diagnostic photo inclus
• Rapports détaillés

👥 **Coopérative (3000 FCFA/mois)**
• Tout du premium
• Fonctionnalités groupe
• Statistiques partagées

**Chaque niveau débloque de nouvelles fonctionnalités !"""
            }
        }
    
    def _load_scenarios(self) -> Dict:
        """Charge les scénarios agricoles"""
        return {
            'mais_plantation': {
                'triggers': ['plantation maïs', 'semis maïs', 'planter maïs'],
                'steps': [
                    "🌱 **Préparation du sol**\n• Labour profond (20-25 cm)\n• Nivellement du terrain\n• Préparation des billons",
                    "🌾 **Semis**\n• Écartement : 80 cm entre rangs\n• Profondeur : 3-5 cm\n• Densité : 60-80 000 plants/ha",
                    "💧 **Irrigation**\n• Arrosage après semis\n• Maintien de l'humidité\n• Éviter l'excès d'eau",
                    "🌿 **Entretien**\n• Désherbage précoce\n• Fertilisation adaptée\n• Surveillance des ravageurs"
                ]
            },
            'mais_recolte': {
                'triggers': ['récolte maïs', 'moisson maïs', 'cueillette maïs'],
                'steps': [
                    "📊 **Évaluation de maturité**\n• Grains bien remplis\n• Teneur en eau < 25%\n• Feuilles desséchées",
                    "🔪 **Récolte**\n• Coupe des tiges\n• Égrenage manuel ou mécanique\n• Tri des grains",
                    "☀️ **Séchage**\n• Séchage au soleil\n• Teneur finale < 14%\n• Stockage aéré",
                    "📦 **Stockage**\n• Conteneurs hermétiques\n• Protection contre les rongeurs\n• Contrôle régulier"
                ]
            },
            'pesticide_application': {
                'triggers': ['pesticide', 'traitement', 'pulvérisation'],
                'steps': [
                    "🔍 **Diagnostic**\n• Identification du problème\n• Choix du produit approprié\n• Lecture de l'étiquette",
                    "🛡️ **Protection**\n• Équipements de protection\n• Conditions météo favorables\n• Respect des délais",
                    "💧 **Application**\n• Dosage précis\n• Couverture complète\n• Éviter la dérive",
                    "📝 **Suivi**\n• Observation des résultats\n• Respect des délais avant récolte\n• Rotation des produits"
                ]
            }
        }
    
    def process_message(self, message: str, user_id: str = None, context: Dict = None) -> Dict:
        """
        Traite un message utilisateur et génère une réponse
        
        Args:
            message (str): Message de l'utilisateur
            user_id (str): ID de l'utilisateur
            context (dict): Contexte de la conversation
            
        Returns:
            dict: Réponse avec intention détectée et actions
        """
        try:
            # Normaliser le message
            normalized_message = self._normalize_message(message)
            
            # Détecter l'intention
            intent, confidence = self._detect_intent(normalized_message)
            
            # Vérifier la FAQ
            faq_match = self._check_faq(normalized_message)
            
            # Vérifier les scénarios
            scenario_match = self._check_scenarios(normalized_message)
            
            # Générer la réponse
            response = self._generate_response(
                intent, confidence, faq_match, scenario_match, 
                normalized_message, context
            )
            
            # Mettre à jour le contexte
            if user_id:
                self._update_context(user_id, intent, normalized_message)
            
            return {
                'response': response,
                'intent': intent,
                'confidence': confidence,
                'faq_match': faq_match is not None,
                'scenario_match': scenario_match is not None,
                'actions': self._get_actions(intent, context)
            }
            
        except Exception as e:
            print(f"Erreur traitement message: {e}")
            return {
                'response': "Désolé, je n'ai pas compris votre demande. Pouvez-vous reformuler ? 🤔",
                'intent': 'unknown',
                'confidence': 0.0,
                'faq_match': False,
                'scenario_match': False,
                'actions': []
            }
    
    def _normalize_message(self, message: str) -> str:
        """Normalise le message pour l'analyse"""
        # Convertir en minuscules
        message = message.lower()
        
        # Supprimer les caractères spéciaux
        message = re.sub(r'[^\w\s]', ' ', message)
        
        # Supprimer les espaces multiples
        message = re.sub(r'\s+', ' ', message).strip()
        
        return message
    
    def _detect_intent(self, message: str) -> Tuple[str, float]:
        """Détecte l'intention du message"""
        best_intent = 'unknown'
        best_confidence = 0.0
        
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                matches = re.findall(pattern, message)
                if matches:
                    confidence = len(matches[0]) / len(message) if matches[0] else 0.0
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent_name
        
        return best_intent, best_confidence
    
    def _check_faq(self, message: str) -> Optional[Dict]:
        """Vérifie si le message correspond à une FAQ"""
        for category, faq_data in self.faq_data.items():
            for question in faq_data['questions']:
                if any(word in message for word in question.split()):
                    return {
                        'category': category,
                        'answer': faq_data['answer']
                    }
        return None
    
    def _check_scenarios(self, message: str) -> Optional[Dict]:
        """Vérifie si le message correspond à un scénario"""
        for scenario_name, scenario_data in self.scenarios.items():
            for trigger in scenario_data['triggers']:
                if trigger in message:
                    return {
                        'scenario': scenario_name,
                        'steps': scenario_data['steps']
                    }
        return None
    
    def _generate_response(self, intent: str, confidence: float, 
                          faq_match: Optional[Dict], scenario_match: Optional[Dict],
                          message: str, context: Dict = None) -> str:
        """Génère une réponse appropriée"""
        
        # Priorité 1: Scénario agricole
        if scenario_match:
            steps = scenario_match['steps']
            response = f"🌾 **Guide : {scenario_match['scenario'].replace('_', ' ').title()}**\n\n"
            for i, step in enumerate(steps, 1):
                response += f"{i}. {step}\n\n"
            response += "Avez-vous des questions sur une étape spécifique ?"
            return response
        
        # Priorité 2: FAQ
        if faq_match:
            return faq_match['answer']
        
        # Priorité 3: Intention détectée
        if intent in self.intents and confidence > 0.3:
            responses = self.intents[intent]['responses']
            return random.choice(responses)
        
        # Réponse par défaut
        return self._get_default_response(message, context)
    
    def _get_default_response(self, message: str, context: Dict = None) -> str:
        """Génère une réponse par défaut"""
        default_responses = [
            "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler votre question ? 🤔",
            "Intéressant ! Pourriez-vous me donner plus de détails sur ce que vous cherchez ? 🤷‍♂️",
            "Je suis spécialisé dans l'agriculture. Avez-vous une question sur vos cultures, la météo, ou un business plan ? 🌾",
            "Je peux vous aider avec les business plans, la météo, le diagnostic des maladies, ou nos packages. Que souhaitez-vous explorer ? 🚜"
        ]
        
        return random.choice(default_responses)
    
    def _get_actions(self, intent: str, context: Dict = None) -> List[str]:
        """Retourne les actions suggérées selon l'intention"""
        actions_map = {
            'business_plan': ['create_business_plan', 'get_user_info'],
            'weather': ['get_weather', 'get_agro_advice'],
            'disease_diagnosis': ['request_photo', 'get_disease_info'],
            'payment': ['show_packages', 'create_payment'],
            'help': ['show_features', 'show_tutorial'],
            'greeting': ['show_welcome', 'show_features']
        }
        
        return actions_map.get(intent, [])
    
    def _update_context(self, user_id: str, intent: str, message: str):
        """Met à jour le contexte de l'utilisateur"""
        if user_id not in self.context:
            self.context[user_id] = {
                'last_intent': intent,
                'last_message': message,
                'conversation_history': [],
                'current_scenario': None
            }
        
        self.context[user_id]['last_intent'] = intent
        self.context[user_id]['last_message'] = message
        self.context[user_id]['conversation_history'].append({
            'message': message,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_user_context(self, user_id: str) -> Dict:
        """Récupère le contexte d'un utilisateur"""
        return self.context.get(user_id, {})
    
    def clear_user_context(self, user_id: str):
        """Efface le contexte d'un utilisateur"""
        if user_id in self.context:
            del self.context[user_id] 