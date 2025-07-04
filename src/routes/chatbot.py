from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import os
import requests
from typing import Optional, Dict, Any
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging
from src.services.gemini_service import GeminiAnalysisService
from src.services.document_generator import DocumentGenerator
from src.models.database import db, User, Conversation, Message, WebhookLog, BusinessPlanTemplate, get_db_connection

logger = logging.getLogger(__name__)

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
        
        # Nouveau système avec Gemini
        try:
            if body.strip():  # Seulement si le message n'est pas vide
                logger.info(f"📱 Message WhatsApp de {from_number}: {body}")
                
                # Messages système à ignorer
                system_messages = ['typing...', 'en ligne', 'online', 'hors ligne', 'offline']
                if body.lower() not in system_messages:
                    # Importer le service WhatsApp
                    from src.services.whatsapp_service import whatsapp_service
                    
                    # Vérifier si c'est une commande /start
                    if body.strip().lower() == '/start':
                        welcome_text = """🤖 *Bienvenue dans le Générateur de Business Plan IA* 

Je peux créer un business plan complet pour votre projet d'entreprise !

📋 *Comment ça marche :*
• Commencez votre message par "Je veux"
• Décrivez votre idée d'entreprise
• Je génère automatiquement votre business plan

💡 *Exemples :*
• "Je veux créer une startup de livraison de repas"
• "Je veux ouvrir un salon de coiffure"
• "Je veux lancer une application mobile"

📄 Vous recevrez 2 fichiers :
• 📊 Business Plan Excel (avec projections financières)
• 📋 PDF Technique (spécifications détaillées)

Tapez votre idée en commençant par "Je veux" pour commencer ! 🚀"""
                        
                        whatsapp_service.send_simple_message(from_number, welcome_text)
                        logger.info(f"✅ Message d'accueil envoyé à {from_number}")
                        
                    # Vérifier si le message commence par "je veux"
                    elif body.strip().lower().startswith('je veux'):
                        # Envoyer le message de bienvenue
                        whatsapp_service.send_welcome_message(from_number, body)
                        
                        # Générer le business plan avec Gemini
                        result = generate_business_plan_with_gemini(body, from_number)
                        
                        if result['success']:
                            business_plan = result['business_plan']
                            files = result['files']
                            
                            # URL de base pour les téléchargements
                            base_url = request.url_root.rstrip('/')
                            
                            # Envoyer le message de succès avec les liens de téléchargement
                            whatsapp_service.send_success_message(
                                from_number, 
                                business_plan, 
                                files, 
                                result['documents_analyzed'],
                                base_url
                            )
                            
                            logger.info(f"✅ Business plan généré avec succès pour {from_number}")
                        else:
                            # Envoyer le message d'erreur
                            whatsapp_service.send_error_message(from_number, result['error'])
                            logger.error(f"❌ Erreur génération pour {from_number}: {result['error']}")
                    
                    else:
                        # Message pour guider l'utilisateur
                        help_text = """❓ *Comment utiliser le générateur de Business Plan :*

🔄 Tapez */start* pour voir le message d'accueil

💡 *Ou commencez votre message par "Je veux"* suivi de votre idée :

✅ *Exemples corrects :*
• "Je veux créer une startup de livraison"
• "Je veux ouvrir un restaurant"
• "Je veux lancer une boutique en ligne"

❌ *Évitez :*
• Messages généraux sans "Je veux"
• Questions simples

Essayez maintenant ! 🚀"""
                        
                        whatsapp_service.send_simple_message(from_number, help_text)
                        logger.info(f"📤 Message d'aide envoyé à {from_number}")
        except Exception as bot_error:
            logger.error(f"💥 Erreur critique génération: {str(bot_error)}")
            try:
                from src.services.whatsapp_service import whatsapp_service
                whatsapp_service.send_system_error_message(from_number)
            except:
                pass
        
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

def get_all_templates():
    """Récupère tous les templates de la base de données."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, category, file_path, file_type, created_at
            FROM business_plan_templates
            WHERE is_active = 1
            ORDER BY created_at DESC
        """)
        
        templates = []
        for row in cursor.fetchall():
            templates.append({
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'file_path': row[3],
                'file_type': row[4],
                'created_at': row[5]
            })
        
        conn.close()
        return templates
    except Exception as e:
        logger.error(f"Erreur récupération templates: {str(e)}")
        return []

def generate_business_plan_with_gemini(user_message, phone_number):
    """Génère un business plan complet avec Gemini basé sur le message utilisateur."""
    try:
        # Récupérer tous les templates
        templates = get_all_templates()
        
        if not templates:
            return {
                'success': False,
                'error': 'Aucun template disponible dans la base de données'
            }
        
        logger.info(f"Génération business plan pour {phone_number}: {len(templates)} templates trouvés")
        
        # Initialiser Gemini
        gemini_service = GeminiAnalysisService()
        
        # Analyser avec Gemini
        analysis_result = gemini_service.analyze_documents_for_business_plan(templates, user_message)
        
        if not analysis_result['success']:
            return {
                'success': False,
                'error': f"Erreur analyse Gemini: {analysis_result.get('error')}"
            }
        
        business_plan_data = analysis_result['business_plan']
        
        # Générer les fichiers
        doc_generator = DocumentGenerator()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_phone = phone_number.replace('+', '').replace(' ', '')
        
        # Générer Excel
        excel_filename = f"business_plan_{safe_phone}_{timestamp}.xlsx"
        excel_path = doc_generator.generate_excel_business_plan(business_plan_data, excel_filename)
        
        # Générer PDF
        pdf_filename = f"business_plan_{safe_phone}_{timestamp}.pdf"
        pdf_path = doc_generator.generate_pdf_business_plan(business_plan_data, pdf_filename)
        
        return {
            'success': True,
            'business_plan': business_plan_data,
            'files': {
                'excel': {
                    'path': excel_path,
                    'filename': excel_filename
                },
                'pdf': {
                    'path': pdf_path,
                    'filename': pdf_filename
                }
            },
            'documents_analyzed': analysis_result['documents_analyzed']
        }
        
    except Exception as e:
        logger.error(f"Erreur génération business plan: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

@chatbot_bp.route('/whatsapp-gemini', methods=['POST'])
def whatsapp_gemini_webhook():
    """
    Webhook WhatsApp avec Gemini AI - génère automatiquement un business plan 
    avec Gemini pour chaque message reçu
    """
    try:
        data = request.get_json() or request.form.to_dict()
        logger.info(f"Webhook WhatsApp Gemini reçu: {data}")
        
        # Format générique - adapter selon votre provider WhatsApp
        # Pour Twilio WhatsApp (form data)
        if 'Body' in data and 'From' in data:
            message = data.get('Body', '').strip()
            phone_number = data.get('From', '').replace('whatsapp:', '')
        # Pour WhatsApp Business API (JSON)
        elif 'messages' in data:
            messages = data.get('messages', [])
            if messages:
                message = messages[0].get('text', {}).get('body', '').strip()
                phone_number = messages[0].get('from', '')
            else:
                message = ''
                phone_number = ''
        # Format personnalisé
        else:
            message = data.get('message', {}).get('text', '').strip()
            phone_number = data.get('from', '')
        
        if not message or not phone_number:
            logger.warning("Message ou numéro manquant dans le webhook")
            return jsonify({'status': 'no_content'}), 200
        
        logger.info(f"📱 Message WhatsApp de {phone_number}: {message}")
        
        # Messages système à ignorer
        system_messages = ['typing...', 'en ligne', 'online', 'hors ligne', 'offline']
        if message.lower() in system_messages:
            return jsonify({'status': 'system_message_ignored'}), 200
        
        # Importer le service WhatsApp
        from src.services.whatsapp_service import whatsapp_service
        
        # Envoyer le message de bienvenue
        whatsapp_service.send_welcome_message(phone_number, message)
        
        # Générer le business plan avec Gemini
        result = generate_business_plan_with_gemini(message, phone_number)
        
        if result['success']:
            business_plan = result['business_plan']
            files = result['files']
            
            # URL de base pour les téléchargements
            base_url = request.url_root.rstrip('/')
            
            # Envoyer le message de succès avec les liens de téléchargement
            whatsapp_service.send_success_message(
                phone_number, 
                business_plan, 
                files, 
                result['documents_analyzed'],
                base_url
            )
            
            logger.info(f"✅ Business plan généré avec succès pour {phone_number}")
            
            return jsonify({
                'status': 'success',
                'message': 'Business plan généré et envoyé',
                'business_plan_title': business_plan.get('titre'),
                'files_generated': 2,
                'documents_analyzed': result['documents_analyzed'],
                'phone_number': phone_number
            }), 200
            
        else:
            # Envoyer le message d'erreur
            whatsapp_service.send_error_message(phone_number, result['error'])
            
            logger.error(f"❌ Erreur génération pour {phone_number}: {result['error']}")
            
            return jsonify({
                'status': 'error',
                'message': result['error'],
                'phone_number': phone_number
            }), 200
        
    except Exception as e:
        logger.error(f"💥 Erreur critique webhook WhatsApp: {str(e)}")
        
        # Envoyer message d'erreur système
        try:
            from src.services.whatsapp_service import whatsapp_service
            whatsapp_service.send_system_error_message(
                phone_number if 'phone_number' in locals() else 'unknown'
            )
        except:
            pass
        
        return jsonify({
            'status': 'system_error',
            'message': str(e)
        }), 500

@chatbot_bp.route('/telegram-gemini', methods=['POST'])
def telegram_gemini_webhook():
    """Webhook pour Telegram avec Gemini AI"""
    try:
        data = request.get_json()
        
        if 'message' in data:
            message_data = data['message']
            text = message_data.get('text', '').strip()
            chat_id = message_data.get('chat', {}).get('id')
            user_name = message_data.get('from', {}).get('first_name', 'Utilisateur')
            
            if not text or not chat_id:
                return jsonify({'status': 'no_content'}), 200
            
            logger.info(f"📱 Message Telegram de {user_name} ({chat_id}): {text}")
            
            # Générer avec Gemini
            result = generate_business_plan_with_gemini(text, str(chat_id))
            
            if result['success']:
                # Message de succès pour Telegram
                telegram_message = f"""🎉 Votre business plan est prêt !

📋 {result['business_plan'].get('titre', 'Business Plan Personnalisé')}

📊 {result['documents_analyzed']} documents analysés
📁 2 fichiers générés (Excel + PDF)

💾 Téléchargement: /download/{result['files']['excel']['filename']}"""
                
                # send_telegram_message(chat_id, telegram_message)
                
            return jsonify({'status': 'success'}), 200
            
    except Exception as e:
        logger.error(f"Erreur webhook Telegram: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@chatbot_bp.route('/messenger-gemini', methods=['POST'])
def messenger_gemini_webhook():
    """Webhook pour Facebook Messenger avec Gemini AI"""
    try:
        data = request.get_json()
        
        if 'entry' in data:
            for entry in data['entry']:
                messaging = entry.get('messaging', [])
                for message_event in messaging:
                    if 'message' in message_event:
                        sender_id = message_event['sender']['id']
                        message_text = message_event['message'].get('text', '').strip()
                        
                        if message_text:
                            logger.info(f"📱 Message Messenger de {sender_id}: {message_text}")
                            
                            # Générer avec Gemini
                            result = generate_business_plan_with_gemini(message_text, sender_id)
                            
                            if result['success']:
                                # Message pour Messenger
                                messenger_message = f"✅ Business plan créé ! Titre: {result['business_plan'].get('titre', 'Plan Personnalisé')}"
                                # send_messenger_message(sender_id, messenger_message)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logger.error(f"Erreur webhook Messenger: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@chatbot_bp.route('/test-generation', methods=['POST'])
def test_generation():
    """Endpoint de test pour la génération de business plan"""
    try:
        data = request.get_json()
        user_message = data.get('message', 'Créer une startup de technologie innovante')
        phone_number = data.get('phone', 'test_user')
        
        result = generate_business_plan_with_gemini(user_message, phone_number)
        
        return jsonify(result), 200 if result['success'] else 500
        
    except Exception as e:
        logger.error(f"Erreur test génération: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Fonctions d'envoi de messages (à implémenter selon votre provider)
def send_whatsapp_message(phone_number, message):
    """Envoie un message WhatsApp - à implémenter selon votre provider"""
    # Exemple pour Twilio
    # client = Client(account_sid, auth_token)
    # client.messages.create(body=message, from_='whatsapp:+14155238886', to=f'whatsapp:{phone_number}')
    logger.info(f"📤 Message WhatsApp à {phone_number}: {message[:100]}...")

def send_whatsapp_document(phone_number, file_path, caption):
    """Envoie un document WhatsApp - à implémenter selon votre provider"""
    logger.info(f"📎 Document WhatsApp à {phone_number}: {file_path}")

def send_telegram_message(chat_id, message):
    """Envoie un message Telegram"""
    logger.info(f"📤 Message Telegram à {chat_id}: {message[:100]}...")

def send_messenger_message(sender_id, message):
    """Envoie un message Messenger"""
    logger.info(f"📤 Message Messenger à {sender_id}: {message[:100]}...")

# Routes alternatives pour les webhooks sans préfixe /api/chatbot  
# Récupération des fonctions originales avant renommage
try:
    # Ces fonctions existent dans le scope global depuis le début du fichier
    telegram_webhook_original = globals()['telegram_webhook']
    messenger_webhook_original = globals()['messenger_webhook']
except KeyError:
    # Si les fonctions n'existent pas, on va les définir comme des stubs
    def telegram_webhook_original():
        return jsonify({'error': 'Function not implemented'}), 501
    def messenger_webhook_original():
        return jsonify({'error': 'Function not implemented'}), 501

# Fonctions pour exposer les webhooks sans préfixe /api/chatbot
def whatsapp_webhook_public():
    return whatsapp_webhook()

def telegram_webhook_public():
    return telegram_webhook_original()

def messenger_webhook_public():
    return messenger_webhook_original()

@chatbot_bp.route('/test-gemini', methods=['POST'])
def test_gemini_generation():
    """Endpoint de test pour la génération avec Gemini"""
    try:
        data = request.get_json() or {}
        test_message = data.get('message', 'Je veux créer une startup de technologie innovante dans le domaine de l\'IA')
        phone_number = data.get('phone', 'test_user_12345')
        
        logger.info(f"🧪 Test Gemini - Message: {test_message}")
        
        # Générer le business plan avec Gemini
        result = generate_business_plan_with_gemini(test_message, phone_number)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Business plan généré avec succès en mode test',
                'business_plan_title': result['business_plan'].get('titre'),
                'files_generated': {
                    'excel': result['files']['excel']['filename'],
                    'pdf': result['files']['pdf']['filename']
                },
                'documents_analyzed': result['documents_analyzed'],
                'download_links': {
                    'excel': f"/download/{result['files']['excel']['filename']}",
                    'pdf': f"/download/{result['files']['pdf']['filename']}"
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'message': 'Erreur lors de la génération du business plan'
            }), 500
            
    except Exception as e:
        logger.error(f"❌ Erreur test Gemini: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur critique lors du test'
        }), 500

