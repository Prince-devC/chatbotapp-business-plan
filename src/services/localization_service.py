"""
Service de localisation pour AgroBizChat
Support des langues locales béninoises
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class LocalizationService:
    """Service de localisation pour les langues locales béninoises"""
    
    def __init__(self):
        self.supported_languages = self._load_supported_languages()
        self.translations = self._load_translations()
        self.agricultural_terms = self._load_agricultural_terms()
        
    def _load_supported_languages(self) -> Dict:
        """Charge les langues supportées"""
        return {
            'fr': {
                'name': 'Français',
                'native_name': 'Français',
                'code': 'fr',
                'direction': 'ltr',
                'flag': '🇫🇷'
            },
            'fon': {
                'name': 'Fon',
                'native_name': 'Fɔ̀ngbè',
                'code': 'fon',
                'direction': 'ltr',
                'flag': '🇧🇯'
            },
            'yor': {
                'name': 'Yoruba',
                'native_name': 'Èdè Yorùbá',
                'code': 'yor',
                'direction': 'ltr',
                'flag': '🇧🇯'
            },
            'min': {
                'name': 'Mina',
                'native_name': 'Gen-Gbe',
                'code': 'min',
                'direction': 'ltr',
                'flag': '🇧🇯'
            },
            'bar': {
                'name': 'Bariba',
                'native_name': 'Baatɔnum',
                'code': 'bar',
                'direction': 'ltr',
                'flag': '🇧🇯'
            }
        }
    
    def _load_translations(self) -> Dict:
        """Charge les traductions"""
        return {
            'fr': {
                'greeting': 'Bonjour ! Je suis AgroBizChat, votre assistant agricole.',
                'welcome': 'Bienvenue dans AgroBizChat !',
                'help': 'Comment puis-je vous aider ?',
                'business_plan': 'Plan d\'affaires',
                'weather': 'Météo',
                'disease': 'Maladie',
                'payment': 'Paiement',
                'settings': 'Paramètres',
                'language': 'Langue',
                'save': 'Enregistrer',
                'cancel': 'Annuler',
                'confirm': 'Confirmer',
                'error': 'Erreur',
                'success': 'Succès',
                'loading': 'Chargement...',
                'not_found': 'Non trouvé',
                'invalid_input': 'Entrée invalide',
                'network_error': 'Erreur réseau',
                'server_error': 'Erreur serveur',
                'timeout': 'Délai d\'attente dépassé'
            },
            'fon': {
                'greeting': 'Bonjour ! N ye AgroBizChat, nɔ̀ ɖɔ̀ hwɛ̀gbɛ̀ ɖɔ̀.',
                'welcome': 'Agoo wá AgroBizChat !',
                'help': 'N ka nyɛ̀ ɖɔ̀ hɛ̀n ?',
                'business_plan': 'Gan ɖɔ̀ hwɛ̀gbɛ̀',
                'weather': 'Xwé',
                'disease': 'Àtɔ̀n',
                'payment': 'Gan',
                'settings': 'Àyìkɔ̀',
                'language': 'Gbɛ̀gbɛ̀',
                'save': 'Kpɔn',
                'cancel': 'Tɔn',
                'confirm': 'Kpɔn',
                'error': 'Àtɔ̀n',
                'success': 'Yé',
                'loading': 'Nɔ̀ ɖɔ̀...',
                'not_found': 'Mɛ̀ ɖɔ̀',
                'invalid_input': 'Àtɔ̀n ɖɔ̀',
                'network_error': 'Àtɔ̀n ɖɔ̀',
                'server_error': 'Àtɔ̀n ɖɔ̀',
                'timeout': 'Àtɔ̀n ɖɔ̀'
            },
            'yor': {
                'greeting': 'Ẹ káàbọ̀ ! Èmi ni AgroBizChat, olùrànlọ́wọ́ ìṣọ̀ọ́gbìn rẹ.',
                'welcome': 'Káàbọ̀ sí AgroBizChat !',
                'help': 'Báwo ni mo ṣe lè ràn yín lọ́wọ́ ?',
                'business_plan': 'Ètò ìṣòwò',
                'weather': 'Òjò',
                'disease': 'Àrùn',
                'payment': 'Ìsanwó',
                'settings': 'Ìṣètò',
                'language': 'Èdè',
                'save': 'Fipamọ́',
                'cancel': 'Fagilé',
                'confirm': 'Jẹ́rìí',
                'error': 'Àsìṣe',
                'success': 'Ìlọ́sí',
                'loading': 'N ṣíṣe...',
                'not_found': 'Kò rí',
                'invalid_input': 'Ìbéèrè tí kò tọ́',
                'network_error': 'Àsìṣe nẹ́tíwọ́ọ̀kì',
                'server_error': 'Àsìṣe sẹ́ẹ̀fà',
                'timeout': 'Àkókò tí kọjá'
            },
            'min': {
                'greeting': 'Bonjour ! N ye AgroBizChat, nɔ̀ ɖɔ̀ hwɛ̀gbɛ̀ ɖɔ̀.',
                'welcome': 'Agoo wá AgroBizChat !',
                'help': 'N ka nyɛ̀ ɖɔ̀ hɛ̀n ?',
                'business_plan': 'Gan ɖɔ̀ hwɛ̀gbɛ̀',
                'weather': 'Xwé',
                'disease': 'Àtɔ̀n',
                'payment': 'Gan',
                'settings': 'Àyìkɔ̀',
                'language': 'Gbɛ̀gbɛ̀',
                'save': 'Kpɔn',
                'cancel': 'Tɔn',
                'confirm': 'Kpɔn',
                'error': 'Àtɔ̀n',
                'success': 'Yé',
                'loading': 'Nɔ̀ ɖɔ̀...',
                'not_found': 'Mɛ̀ ɖɔ̀',
                'invalid_input': 'Àtɔ̀n ɖɔ̀',
                'network_error': 'Àtɔ̀n ɖɔ̀',
                'server_error': 'Àtɔ̀n ɖɔ̀',
                'timeout': 'Àtɔ̀n ɖɔ̀'
            },
            'bar': {
                'greeting': 'Bonjour ! N ye AgroBizChat, nɔ̀ ɖɔ̀ hwɛ̀gbɛ̀ ɖɔ̀.',
                'welcome': 'Agoo wá AgroBizChat !',
                'help': 'N ka nyɛ̀ ɖɔ̀ hɛ̀n ?',
                'business_plan': 'Gan ɖɔ̀ hwɛ̀gbɛ̀',
                'weather': 'Xwé',
                'disease': 'Àtɔ̀n',
                'payment': 'Gan',
                'settings': 'Àyìkɔ̀',
                'language': 'Gbɛ̀gbɛ̀',
                'save': 'Kpɔn',
                'cancel': 'Tɔn',
                'confirm': 'Kpɔn',
                'error': 'Àtɔ̀n',
                'success': 'Yé',
                'loading': 'Nɔ̀ ɖɔ̀...',
                'not_found': 'Mɛ̀ ɖɔ̀',
                'invalid_input': 'Àtɔ̀n ɖɔ̀',
                'network_error': 'Àtɔ̀n ɖɔ̀',
                'server_error': 'Àtɔ̀n ɖɔ̀',
                'timeout': 'Àtɔ̀n ɖɔ̀'
            }
        }
    
    def _load_agricultural_terms(self) -> Dict:
        """Charge la terminologie agricole"""
        return {
            'fr': {
                'corn': 'Maïs',
                'pineapple': 'Ananas',
                'agriculture': 'Agriculture',
                'farmer': 'Agriculteur',
                'farm': 'Ferme',
                'crop': 'Culture',
                'harvest': 'Récolte',
                'planting': 'Plantation',
                'irrigation': 'Irrigation',
                'fertilizer': 'Engrais',
                'pesticide': 'Pesticide',
                'soil': 'Sol',
                'weather': 'Météo',
                'rain': 'Pluie',
                'sun': 'Soleil',
                'disease': 'Maladie',
                'treatment': 'Traitement',
                'prevention': 'Prévention',
                'yield': 'Rendement',
                'profit': 'Profit',
                'cost': 'Coût',
                'price': 'Prix',
                'market': 'Marché',
                'business_plan': 'Plan d\'affaires',
                'investment': 'Investissement',
                'loan': 'Prêt',
                'cooperative': 'Coopérative',
                'extension': 'Vulgarisation',
                'training': 'Formation',
                'technology': 'Technologie'
            },
            'fon': {
                'corn': 'Kpɛn',
                'pineapple': 'Anana',
                'agriculture': 'Agbɔ̀',
                'farmer': 'Agbɔ̀tɔ',
                'farm': 'Agbɔ̀',
                'crop': 'Gan',
                'harvest': 'Gan',
                'planting': 'Gan',
                'irrigation': 'Tɔ̀',
                'fertilizer': 'Gan',
                'pesticide': 'Gan',
                'soil': 'Tɔ̀',
                'weather': 'Xwé',
                'rain': 'Jí',
                'sun': 'Xwé',
                'disease': 'Àtɔ̀n',
                'treatment': 'Gan',
                'prevention': 'Gan',
                'yield': 'Gan',
                'profit': 'Gan',
                'cost': 'Gan',
                'price': 'Gan',
                'market': 'Gan',
                'business_plan': 'Gan ɖɔ̀ hwɛ̀gbɛ̀',
                'investment': 'Gan',
                'loan': 'Gan',
                'cooperative': 'Gan',
                'extension': 'Gan',
                'training': 'Gan',
                'technology': 'Gan'
            },
            'yor': {
                'corn': 'Ọkà',
                'pineapple': 'Ọ̀gbẹ̀dẹ̀',
                'agriculture': 'Ìṣọ̀ọ́gbìn',
                'farmer': 'Olùgbìn',
                'farm': 'Ìgbó',
                'crop': 'Ọ̀gbìn',
                'harvest': 'Ìkó',
                'planting': 'Ìgbìn',
                'irrigation': 'Ìṣan omi',
                'fertilizer': 'Àjílẹ̀',
                'pesticide': 'Oògùn',
                'soil': 'Ilẹ̀',
                'weather': 'Òjò',
                'rain': 'Òjò',
                'sun': 'Òòrùn',
                'disease': 'Àrùn',
                'treatment': 'Ìwọ̀sàn',
                'prevention': 'Ìdẹ́nu',
                'yield': 'Ìdá',
                'profit': 'Èrè',
                'cost': 'Ìnà',
                'price': 'Ìyá',
                'market': 'Ọjà',
                'business_plan': 'Ètò ìṣòwò',
                'investment': 'Ìdíwọ́n',
                'loan': 'Ìgbéyàwó',
                'cooperative': 'Ìṣọ̀kan',
                'extension': 'Ìtànkálẹ̀',
                'training': 'Ìkẹ́kọ̀ọ́',
                'technology': 'Ìmọ̀ ìṣẹ́'
            },
            'min': {
                'corn': 'Kpɛn',
                'pineapple': 'Anana',
                'agriculture': 'Agbɔ̀',
                'farmer': 'Agbɔ̀tɔ',
                'farm': 'Agbɔ̀',
                'crop': 'Gan',
                'harvest': 'Gan',
                'planting': 'Gan',
                'irrigation': 'Tɔ̀',
                'fertilizer': 'Gan',
                'pesticide': 'Gan',
                'soil': 'Tɔ̀',
                'weather': 'Xwé',
                'rain': 'Jí',
                'sun': 'Xwé',
                'disease': 'Àtɔ̀n',
                'treatment': 'Gan',
                'prevention': 'Gan',
                'yield': 'Gan',
                'profit': 'Gan',
                'cost': 'Gan',
                'price': 'Gan',
                'market': 'Gan',
                'business_plan': 'Gan ɖɔ̀ hwɛ̀gbɛ̀',
                'investment': 'Gan',
                'loan': 'Gan',
                'cooperative': 'Gan',
                'extension': 'Gan',
                'training': 'Gan',
                'technology': 'Gan'
            },
            'bar': {
                'corn': 'Kpɛn',
                'pineapple': 'Anana',
                'agriculture': 'Agbɔ̀',
                'farmer': 'Agbɔ̀tɔ',
                'farm': 'Agbɔ̀',
                'crop': 'Gan',
                'harvest': 'Gan',
                'planting': 'Gan',
                'irrigation': 'Tɔ̀',
                'fertilizer': 'Gan',
                'pesticide': 'Gan',
                'soil': 'Tɔ̀',
                'weather': 'Xwé',
                'rain': 'Jí',
                'sun': 'Xwé',
                'disease': 'Àtɔ̀n',
                'treatment': 'Gan',
                'prevention': 'Gan',
                'yield': 'Gan',
                'profit': 'Gan',
                'cost': 'Gan',
                'price': 'Gan',
                'market': 'Gan',
                'business_plan': 'Gan ɖɔ̀ hwɛ̀gbɛ̀',
                'investment': 'Gan',
                'loan': 'Gan',
                'cooperative': 'Gan',
                'extension': 'Gan',
                'training': 'Gan',
                'technology': 'Gan'
            }
        }
    
    def get_supported_languages(self) -> Dict:
        """Récupère les langues supportées"""
        return self.supported_languages
    
    def get_language_info(self, lang_code: str) -> Optional[Dict]:
        """Récupère les informations d'une langue"""
        return self.supported_languages.get(lang_code)
    
    def translate(self, key: str, lang_code: str = 'fr', fallback: str = None) -> str:
        """
        Traduit une clé dans la langue spécifiée
        
        Args:
            key (str): Clé à traduire
            lang_code (str): Code de langue
            fallback (str): Texte de fallback
            
        Returns:
            str: Texte traduit
        """
        if lang_code not in self.translations:
            lang_code = 'fr'  # Fallback vers français
        
        translation = self.translations[lang_code].get(key)
        
        if translation:
            return translation
        elif fallback:
            return fallback
        else:
            return key
    
    def translate_agricultural_term(self, term: str, lang_code: str = 'fr') -> str:
        """
        Traduit un terme agricole
        
        Args:
            term (str): Terme à traduire
            lang_code (str): Code de langue
            
        Returns:
            str: Terme traduit
        """
        if lang_code not in self.agricultural_terms:
            lang_code = 'fr'
        
        return self.agricultural_terms[lang_code].get(term, term)
    
    def get_greeting(self, lang_code: str = 'fr') -> str:
        """Récupère une salutation dans la langue spécifiée"""
        return self.translate('greeting', lang_code)
    
    def get_help_message(self, lang_code: str = 'fr') -> str:
        """Récupère un message d'aide dans la langue spécifiée"""
        return self.translate('help', lang_code)
    
    def translate_business_plan_terms(self, lang_code: str = 'fr') -> Dict:
        """Traduit les termes de business plan"""
        terms = [
            'business_plan', 'investment', 'profit', 'cost', 'yield',
            'market', 'price', 'cooperative', 'loan'
        ]
        
        return {
            term: self.translate_agricultural_term(term, lang_code)
            for term in terms
        }
    
    def translate_weather_terms(self, lang_code: str = 'fr') -> Dict:
        """Traduit les termes météo"""
        terms = ['weather', 'rain', 'sun', 'soil']
        
        return {
            term: self.translate_agricultural_term(term, lang_code)
            for term in terms
        }
    
    def translate_disease_terms(self, lang_code: str = 'fr') -> Dict:
        """Traduit les termes de maladie"""
        terms = ['disease', 'treatment', 'prevention']
        
        return {
            term: self.translate_agricultural_term(term, lang_code)
            for term in terms
        }
    
    def detect_language(self, text: str) -> str:
        """
        Détecte la langue d'un texte (basique)
        
        Args:
            text (str): Texte à analyser
            
        Returns:
            str: Code de langue détecté
        """
        # Détection basique basée sur les caractères
        if any(char in text for char in ['ɛ', 'ɔ', 'ɖ', 'ɣ', 'ŋ']):
            return 'fon'  # Caractères Fon
        elif any(char in text for char in ['ẹ', 'ọ', 'ṣ', 'ẹ']):
            return 'yor'  # Caractères Yoruba
        else:
            return 'fr'  # Français par défaut
    
    def format_number(self, number: float, lang_code: str = 'fr') -> str:
        """
        Formate un nombre selon la langue
        
        Args:
            number (float): Nombre à formater
            lang_code (str): Code de langue
            
        Returns:
            str: Nombre formaté
        """
        if lang_code in ['fon', 'yor', 'min', 'bar']:
            # Utiliser le format français pour les langues locales
            return f"{number:,.0f}"
        else:
            return f"{number:,.0f}"
    
    def format_currency(self, amount: float, lang_code: str = 'fr') -> str:
        """
        Formate une monnaie selon la langue
        
        Args:
            amount (float): Montant à formater
            lang_code (str): Code de langue
            
        Returns:
            str: Montant formaté
        """
        formatted_amount = self.format_number(amount, lang_code)
        
        if lang_code == 'yor':
            return f"₦{formatted_amount}"
        else:
            return f"{formatted_amount} FCFA"
    
    def get_localized_response(self, response_type: str, lang_code: str = 'fr', **kwargs) -> str:
        """
        Génère une réponse localisée
        
        Args:
            response_type (str): Type de réponse
            lang_code (str): Code de langue
            **kwargs: Variables pour la réponse
            
        Returns:
            str: Réponse localisée
        """
        if response_type == 'greeting':
            return self.get_greeting(lang_code)
        
        elif response_type == 'business_plan_intro':
            if lang_code == 'fon':
                return f"Bonjour ! N ye AgroBizChat. N ka nyɛ̀ ɖɔ̀ hwɛ̀gbɛ̀ ɖɔ̀ hɛ̀n ?"
            elif lang_code == 'yor':
                return f"Ẹ káàbọ̀ ! Èmi ni AgroBizChat. Báwo ni mo ṣe lè ràn yín lọ́wọ́ ?"
            else:
                return f"Bonjour ! Je suis AgroBizChat. Comment puis-je vous aider ?"
        
        elif response_type == 'weather_info':
            weather_terms = self.translate_weather_terms(lang_code)
            if lang_code == 'fon':
                return f"N ka nyɛ̀ xwé ɖɔ̀ hɛ̀n. {weather_terms['weather']} ɖɔ̀ nyɛ̀."
            elif lang_code == 'yor':
                return f"Mo lè fún yín ní ìròyìn òjò. {weather_terms['weather']} yẹn."
            else:
                return f"Je peux vous donner des informations météo. {weather_terms['weather']} disponible."
        
        elif response_type == 'disease_diagnosis':
            disease_terms = self.translate_disease_terms(lang_code)
            if lang_code == 'fon':
                return f"N ka nyɛ̀ àtɔ̀n ɖɔ̀ hɛ̀n. {disease_terms['disease']} ɖɔ̀ nyɛ̀."
            elif lang_code == 'yor':
                return f"Mo lè ṣe ìwádìí àrùn. {disease_terms['disease']} yẹn."
            else:
                return f"Je peux diagnostiquer les maladies. {disease_terms['disease']} disponible."
        
        else:
            return self.translate('help', lang_code) 