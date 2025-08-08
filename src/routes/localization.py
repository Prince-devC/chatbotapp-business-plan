"""
Routes pour la localisation et support multilingue
Langues locales béninoises
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.localization_service import LocalizationService

localization_bp = Blueprint('localization', __name__)

# Initialiser le service
localization_service = LocalizationService()

@localization_bp.route('/languages', methods=['GET'])
def get_supported_languages():
    """
    Récupère les langues supportées
    """
    try:
        languages = localization_service.get_supported_languages()
        
        return jsonify({
            'success': True,
            'languages': languages
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur récupération langues: {str(e)}'
        }), 500

@localization_bp.route('/translate', methods=['POST'])
def translate_text():
    """
    Traduit un texte
    """
    try:
        data = request.get_json()
        key = data.get('key')
        lang_code = data.get('language', 'fr')
        fallback = data.get('fallback')
        
        if not key:
            return jsonify({
                'success': False,
                'error': 'Clé de traduction manquante'
            }), 400
        
        translation = localization_service.translate(key, lang_code, fallback)
        
        return jsonify({
            'success': True,
            'translation': translation,
            'language': lang_code,
            'key': key
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur traduction: {str(e)}'
        }), 500

@localization_bp.route('/translate/agricultural', methods=['POST'])
def translate_agricultural_term():
    """
    Traduit un terme agricole
    """
    try:
        data = request.get_json()
        term = data.get('term')
        lang_code = data.get('language', 'fr')
        
        if not term:
            return jsonify({
                'success': False,
                'error': 'Terme agricole manquant'
            }), 400
        
        translation = localization_service.translate_agricultural_term(term, lang_code)
        
        return jsonify({
            'success': True,
            'translation': translation,
            'language': lang_code,
            'term': term
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur traduction terme agricole: {str(e)}'
        }), 500

@localization_bp.route('/translate/business-plan', methods=['GET'])
def get_business_plan_translations():
    """
    Récupère les traductions pour les business plans
    """
    try:
        lang_code = request.args.get('language', 'fr')
        
        translations = localization_service.translate_business_plan_terms(lang_code)
        
        return jsonify({
            'success': True,
            'translations': translations,
            'language': lang_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur traductions business plan: {str(e)}'
        }), 500

@localization_bp.route('/translate/weather', methods=['GET'])
def get_weather_translations():
    """
    Récupère les traductions pour la météo
    """
    try:
        lang_code = request.args.get('language', 'fr')
        
        translations = localization_service.translate_weather_terms(lang_code)
        
        return jsonify({
            'success': True,
            'translations': translations,
            'language': lang_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur traductions météo: {str(e)}'
        }), 500

@localization_bp.route('/translate/disease', methods=['GET'])
def get_disease_translations():
    """
    Récupère les traductions pour les maladies
    """
    try:
        lang_code = request.args.get('language', 'fr')
        
        translations = localization_service.translate_disease_terms(lang_code)
        
        return jsonify({
            'success': True,
            'translations': translations,
            'language': lang_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur traductions maladies: {str(e)}'
        }), 500

@localization_bp.route('/detect-language', methods=['POST'])
def detect_language():
    """
    Détecte la langue d'un texte
    """
    try:
        data = request.get_json()
        text = data.get('text')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Texte manquant'
            }), 400
        
        detected_lang = localization_service.detect_language(text)
        
        return jsonify({
            'success': True,
            'detected_language': detected_lang,
            'text': text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur détection langue: {str(e)}'
        }), 500

@localization_bp.route('/format/number', methods=['POST'])
def format_number():
    """
    Formate un nombre selon la langue
    """
    try:
        data = request.get_json()
        number = data.get('number')
        lang_code = data.get('language', 'fr')
        
        if number is None:
            return jsonify({
                'success': False,
                'error': 'Nombre manquant'
            }), 400
        
        formatted_number = localization_service.format_number(number, lang_code)
        
        return jsonify({
            'success': True,
            'formatted_number': formatted_number,
            'language': lang_code,
            'original_number': number
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur formatage nombre: {str(e)}'
        }), 500

@localization_bp.route('/format/currency', methods=['POST'])
def format_currency():
    """
    Formate une monnaie selon la langue
    """
    try:
        data = request.get_json()
        amount = data.get('amount')
        lang_code = data.get('language', 'fr')
        
        if amount is None:
            return jsonify({
                'success': False,
                'error': 'Montant manquant'
            }), 400
        
        formatted_currency = localization_service.format_currency(amount, lang_code)
        
        return jsonify({
            'success': True,
            'formatted_currency': formatted_currency,
            'language': lang_code,
            'original_amount': amount
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur formatage monnaie: {str(e)}'
        }), 500

@localization_bp.route('/response/<response_type>', methods=['GET'])
def get_localized_response(response_type):
    """
    Récupère une réponse localisée
    """
    try:
        lang_code = request.args.get('language', 'fr')
        
        response = localization_service.get_localized_response(response_type, lang_code)
        
        return jsonify({
            'success': True,
            'response': response,
            'response_type': response_type,
            'language': lang_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur réponse localisée: {str(e)}'
        }), 500

@localization_bp.route('/greeting', methods=['GET'])
def get_greeting():
    """
    Récupère une salutation localisée
    """
    try:
        lang_code = request.args.get('language', 'fr')
        
        greeting = localization_service.get_greeting(lang_code)
        
        return jsonify({
            'success': True,
            'greeting': greeting,
            'language': lang_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur salutation: {str(e)}'
        }), 500

@localization_bp.route('/help', methods=['GET'])
def get_help_message():
    """
    Récupère un message d'aide localisé
    """
    try:
        lang_code = request.args.get('language', 'fr')
        
        help_message = localization_service.get_help_message(lang_code)
        
        return jsonify({
            'success': True,
            'help_message': help_message,
            'language': lang_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur message d\'aide: {str(e)}'
        }), 500 