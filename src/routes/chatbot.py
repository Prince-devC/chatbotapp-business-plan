from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import os
import requests
from typing import Optional, Dict, Any
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from src.models.database import db, User, Conversation, Message, WebhookLog, BusinessPlanTemplate

chatbot_bp = Blueprint('chatbot', __name__)

def send_telegram_message(chat_id: str, text: str) -> Optional[Dict[str, Any]]:
    """Envoyer un message via l'API Telegram"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        response = requests.post(url, json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        })
        return response.json() if response.ok else None
    except Exception as e:
        print(f"Erreur lors de l'envoi du message Telegram: {str(e)}")
        return None

def send_whatsapp_message(to: str, text: str) -> Optional[Dict[str, Any]]:
    """Envoyer un message via l'API Twilio WhatsApp"""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_number]):
        print("Configuration Twilio manquante")
        return None
        
    # Nettoyer et formater les numéros de téléphone
    def clean_phone_number(number: str) -> str:
        # Enlever 'whatsapp:', les espaces et les caractères non numériques
        clean = ''.join(c for c in number.replace('whatsapp:', '') if c.isdigit())
        # S'assurer que le numéro commence par '+'
        if not clean.startswith('+'):
            clean = '+' + clean
        return clean
        
    try:
        # Nettoyer les numéros
        clean_from = clean_phone_number(from_number)
        clean_to = clean_phone_number(to)
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=f'whatsapp:{clean_from}',
            body=text,
            to=f'whatsapp:{clean_to}'
        )
        return {'sid': message.sid, 'status': message.status}
    except TwilioRestException as e:
        print(f"Erreur Twilio lors de l'envoi du message WhatsApp: {str(e)}")
        return None
    except Exception as e:
        print(f"Erreur lors de l'envoi du message WhatsApp: {str(e)}")
        return None

def process_bot_response(conversation: Conversation, message: Message) -> None:
    """Traiter la réponse du bot"""
    try:
        # Récupérer le texte du message de l'utilisateur
        user_message = message.content.lower() if message.content else ''
        chat_id = conversation.session_id
        
        # Message de bienvenue pour /start
        if user_message == '/start':
            response_text = (
                "👋 Bonjour ! Je suis votre assistant pour la création de business plan.\n\n"
                "Je peux vous aider à :\n"
                "📝 Créer un business plan\n"
                "📊 Analyser votre marché\n"
                "💡 Suggérer des idées pour votre entreprise\n\n"
                "Pour commencer, dites-moi simplement ce que vous souhaitez faire !"
            )
        # Message d'aide
        elif user_message == '/help':
            response_text = (
                "Voici les commandes disponibles :\n\n"
                "/start - Démarrer une nouvelle conversation\n"
                "/help - Afficher ce message d'aide\n"
                "/templates - Voir les modèles de business plan disponibles\n"
                "/cancel - Annuler l'opération en cours"
            )
        # Liste des templates
        elif user_message == '/templates':
            templates = BusinessPlanTemplate.query.filter_by(is_active=True).all()
            if templates:
                response_text = "📋 Modèles de business plan disponibles :\n\n"
                for template in templates:
                    response_text += f"- {template.name}: {template.description}\n"
            else:
                response_text = "Aucun modèle disponible pour le moment."
        # Réponse par défaut
        else:
            response_text = (
                "Je ne suis pas encore configuré pour répondre à ce type de message. "
                "Utilisez /help pour voir les commandes disponibles."
            )
        
        # Envoyer la réponse via la bonne plateforme
        sent = False
        if conversation.user.platform == 'telegram':
            sent = bool(send_telegram_message(chat_id, response_text))
        elif conversation.user.platform == 'whatsapp':
            sent = bool(send_whatsapp_message(chat_id, response_text))
        
        if sent:
            # Enregistrer la réponse du bot dans la base de données
            bot_message = Message(
                conversation_id=conversation.id,
                sender='bot',
                message_type='text',
                content=response_text
            )
            db.session.add(bot_message)
            db.session.commit()
            
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors du traitement de la réponse du bot: {str(e)}")

@chatbot_bp.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    """Webhook pour recevoir les messages Telegram"""
    log = None
    
    try:
        # Reset any stale transaction state
        db.session.remove()
        
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        if 'message' not in data:
            return jsonify({'error': 'Invalid webhook data: no message found'}), 400

        # Initialize webhook log
        log = WebhookLog(
            platform='telegram',
            webhook_data='{}',  # Initialize with empty string
            processed=False,
            error_message=None
        )
        
        try:
            # Save webhook data
            log.set_webhook_data(data)
            db.session.add(log)
            db.session.flush()
            
            # Get message data
            message_data = data['message']
            user_data = message_data.get('from', {})
            chat_data = message_data.get('chat', {})
            
            # Validate required fields
            if not user_data.get('id') or not chat_data.get('id'):
                raise ValueError('Missing required user or chat ID in webhook data')
            
            # Create or get user
            user = get_or_create_user(
                platform='telegram',
                platform_user_id=str(user_data.get('id')),
                username=user_data.get('username'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                language_code=user_data.get('language_code', 'fr')
            )
            
            # Create or get conversation
            conversation = get_or_create_conversation(user.id, str(chat_data.get('id')))
            
            # Create message
            message = Message(
                conversation_id=conversation.id,
                sender='user',
                message_type='text',
                content=message_data.get('text', '')
            )
            
            # Handle media types
            if 'photo' in message_data:
                message.message_type = 'image'
                message.set_metadata({'photo': message_data['photo']})
            elif 'document' in message_data:
                message.message_type = 'document'
                message.set_metadata({'document': message_data['document']})
            
            # Save message
            db.session.add(message)
            
            # Mark webhook as processed
            log.processed = True
            
            # Commit all changes
            db.session.commit()
            
            try:
                # Process bot response in a separate transaction
                process_bot_response(conversation, message)
            except Exception as bot_error:
                print(f"Error in bot response: {str(bot_error)}")
                # Don't fail the webhook just because the bot response failed
            
            return jsonify({'status': 'ok'}), 200
            
        except Exception as e:
            db.session.rollback()
            if log:
                log.error_message = str(e)
                db.session.add(log)
                db.session.commit()
            raise
            
    except Exception as e:
        error_msg = str(e)
        print(f"Telegram webhook error: {error_msg}")
        
        # Try to log the error if we haven't already
        if log is None:
            try:
                log = WebhookLog(
                    platform='telegram',
                    webhook_data='{}',
                    processed=False,
                    error_message=error_msg
                )
                if data:
                    log.set_webhook_data(data)
                db.session.add(log)
                db.session.commit()
            except Exception as log_error:
                print(f"Failed to log webhook error: {str(log_error)}")
        
        return jsonify({
            'error': 'Internal server error',
            'details': error_msg
        }), 500

@chatbot_bp.route('/webhook/messenger', methods=['POST'])
def messenger_webhook():
    """Webhook pour recevoir les messages Facebook Messenger"""
    try:
        data = request.get_json()
        
        # Logger le webhook
        log = WebhookLog(
            platform='messenger',
            webhook_data={}
        )
        log.set_webhook_data(data)
        db.session.add(log)
        
        # Traiter les entrées
        if 'entry' in data:
            for entry in data['entry']:
                if 'messaging' in entry:
                    for messaging_event in entry['messaging']:
                        if 'message' in messaging_event:
                            process_messenger_message(messaging_event)
        
        log.processed = True
        db.session.commit()
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        if 'log' in locals():
            log.error_message = str(e)
            db.session.commit()
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Webhook pour recevoir les messages Twilio WhatsApp"""
    log = None
    
    try:
        # Validate Twilio request
        form_data = request.form.to_dict()
        
        # Logger le webhook
        log = WebhookLog(
            platform='whatsapp',
            webhook_data='{}',
            processed=False,
            error_message=None
        )
        log.set_webhook_data(form_data)
        db.session.add(log)
        db.session.flush()
        
        # Extraire les données du message
        message_sid = form_data.get('MessageSid')
        from_number = form_data.get('From', '').replace('whatsapp:', '')
        body = form_data.get('Body', '')
        
        if not all([message_sid, from_number]):
            raise ValueError('Missing required WhatsApp message data')
        
        # Créer ou récupérer l'utilisateur
        user = get_or_create_user(
            platform='whatsapp',
            platform_user_id=from_number,
            phone_number=from_number
        )
        
        # Créer ou récupérer la conversation
        conversation = get_or_create_conversation(user.id, from_number)
        
        # Enregistrer le message
        message = Message(
            conversation_id=conversation.id,
            sender='user',
            message_type='text',
            content=body,
        )
        
        # Gérer les médias
        if 'MediaUrl0' in form_data:
            message.message_type = 'media'
            media_data = {
                'url': form_data.get('MediaUrl0'),
                'content_type': form_data.get('MediaContentType0'),
                'sid': form_data.get('MediaSid0')
            }
            message.set_metadata(media_data)
        
        db.session.add(message)
        
        # Marquer le webhook comme traité
        log.processed = True
        
        # Commit all changes
        db.session.commit()
        
        try:
            # Process bot response in a separate transaction
            process_bot_response(conversation, message)
        except Exception as bot_error:
            print(f"Error in bot response: {str(bot_error)}")
            # Don't fail the webhook just because the bot response failed
        
        return '', 204
        
    except Exception as e:
        error_msg = str(e)
        print(f"WhatsApp webhook error: {error_msg}")
        
        if log:
            db.session.rollback()
            log.error_message = error_msg
            db.session.add(log)
            db.session.commit()
        
        return jsonify({'error': 'Internal server error', 'details': error_msg}), 500

def process_whatsapp_message(message: Dict[str, Any]) -> None:
    """Traiter un message WhatsApp entrant"""
    try:
        # Extraire les informations du message
        from_number = message.get('from')
        message_type = message.get('type')
        message_content = message.get('text', {}).get('body', '') if message_type == 'text' else ''
        
        if not from_number:
            raise ValueError('Missing sender phone number in message')
        
        # Créer ou récupérer l'utilisateur
        user = get_or_create_user(
            platform='whatsapp',
            platform_user_id=from_number,
            phone_number=from_number
        )
        
        # Créer ou récupérer la conversation
        conversation = get_or_create_conversation(user.id, from_number)
        
        # Créer le message
        db_message = Message(
            conversation_id=conversation.id,
            sender='user',
            message_type=message_type,
            content=message_content
        )
        
        # Gérer les types de médias
        if message_type == 'image':
            db_message.set_metadata({'image': message.get('image', {})})
        elif message_type == 'document':
            db_message.set_metadata({'document': message.get('document', {})})
        
        # Sauvegarder le message
        db.session.add(db_message)
        db.session.commit()
        
        # Traiter la réponse du bot
        process_bot_response(conversation, db_message)
        
    except Exception as e:
        db.session.rollback()
        print(f"Error processing WhatsApp message: {str(e)}")
        raise

@chatbot_bp.route('/webhook/messenger', methods=['GET'])
def messenger_webhook_verify():
    """Vérification du webhook Facebook Messenger"""
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Token de vérification (à configurer dans les variables d'environnement)
    expected_token = "your_verify_token_here"
    
    if verify_token == expected_token:
        return challenge
    else:
        return "Verification failed", 403

@chatbot_bp.route('/webhook/whatsapp', methods=['GET'])
def whatsapp_webhook_verify():
    """Vérification du webhook WhatsApp Business"""
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Token de vérification (à configurer dans les variables d'environnement)
    expected_token = "your_whatsapp_verify_token_here"
    
    if verify_token == expected_token:
        return challenge
    else:
        return "Verification failed", 403

@chatbot_bp.route('/users', methods=['GET'])
def get_users():
    """Récupérer la liste des utilisateurs"""
    platform = request.args.get('platform')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    query = User.query
    if platform:
        query = query.filter_by(platform=platform)
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    }), 200

@chatbot_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Récupérer la liste des conversations"""
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    query = Conversation.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    conversations = query.order_by(Conversation.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'conversations': [conv.to_dict() for conv in conversations.items],
        'total': conversations.total,
        'pages': conversations.pages,
        'current_page': page
    }), 200

@chatbot_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Récupérer les messages d'une conversation"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    
    messages = Message.query.filter_by(conversation_id=conversation_id)\
        .order_by(Message.created_at.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'messages': [msg.to_dict() for msg in messages.items],
        'total': messages.total,
        'pages': messages.pages,
        'current_page': page
    }), 200

def get_or_create_user(platform, platform_user_id, **kwargs):
    """Créer ou récupérer un utilisateur"""
    try:
        # Try to find existing user
        user = User.query.filter_by(
            platform=platform,
            platform_user_id=platform_user_id
        ).first()
        
        if not user:
            # Create new user
            user = User(
                platform=platform,
                platform_user_id=platform_user_id,
                **kwargs
            )
            db.session.add(user)
        else:
            # Update existing user
            user.last_interaction = datetime.utcnow()
            
            # Update changed information
            for key, value in kwargs.items():
                if hasattr(user, key) and value:
                    setattr(user, key, value)
        
        # Commit to ensure user has an ID
        db.session.commit()
        return user
        
    except Exception as e:
        db.session.rollback()
        raise

def get_or_create_conversation(user_id, session_id):
    """Créer ou récupérer une conversation"""
    try:
        if not user_id:
            raise ValueError("user_id cannot be None")
        if not session_id:
            raise ValueError("session_id cannot be None")
            
        # Try to find existing conversation
        conversation = Conversation.query.filter_by(
            user_id=user_id,
            session_id=session_id,
            status='active'
        ).first()
        
        if not conversation:
            # Create new conversation
            conversation = Conversation(
                user_id=user_id,
                session_id=session_id,
                status='active',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(conversation)
        else:
            # Update existing conversation
            conversation.updated_at = datetime.utcnow()
        
        # Commit changes
        db.session.commit()
        return conversation
        
    except Exception as e:
        db.session.rollback()
        raise

def process_messenger_message(messaging_event):
    """Traiter un message Facebook Messenger"""
    try:
        sender_id = messaging_event['sender']['id']
        message_data = messaging_event['message']
        
        # Créer ou récupérer l'utilisateur
        user = get_or_create_user(
            platform='messenger',
            platform_user_id=sender_id
        )
        
        # Créer ou récupérer la conversation
        conversation = get_or_create_conversation(user.id, sender_id)
        
        # Enregistrer le message
        message = Message(
            conversation_id=conversation.id,
            sender='user',
            message_type='text',
            content=message_data.get('text', '')
        )
        
        if 'attachments' in message_data:
            message.message_type = 'attachment'
            message.set_metadata({'attachments': message_data['attachments']})
        
        db.session.add(message)
        db.session.commit()
        
        # Process bot response
        process_bot_response(conversation, message)
        
    except Exception as e:
        db.session.rollback()
        raise

# Route alternative pour le webhook WhatsApp (compatibilité)
@chatbot_bp.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook_alt():
    """Route alternative pour le webhook WhatsApp"""
    return whatsapp_webhook()

