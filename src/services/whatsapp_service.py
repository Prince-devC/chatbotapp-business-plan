import os
import logging
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        # Configuration Twilio
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        if not self.account_sid or not self.auth_token:
            logger.warning("Configuration Twilio manquante - messages WhatsApp simulés uniquement")
            self.client = None
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Service WhatsApp Twilio initialisé avec succès")
            except Exception as e:
                logger.error(f"Erreur initialisation Twilio: {str(e)}")
                self.client = None
    
    def send_message(self, to_number: str, message: str) -> bool:
        """Envoie un message WhatsApp via Twilio."""
        try:
            if not self.client:
                logger.info(f"📤 [SIMULÉ] Message WhatsApp à {to_number}: {message[:100]}...")
                return True
            
            # Normaliser le numéro
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            # Envoyer le message
            message_instance = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=to_number
            )
            
            logger.info(f"✅ Message WhatsApp envoyé - SID: {message_instance.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"❌ Erreur Twilio: {e.msg} (Code: {e.code})")
            
            # Gérer spécifiquement la limite quotidienne
            if e.code == 63038:
                logger.warning("📊 Limite quotidienne Twilio atteinte - Mode simulation activé")
                logger.info(f"📤 [SIMULÉ - LIMITE] Message WhatsApp à {to_number}: {message[:100]}...")
                return True
            
            return False
        except Exception as e:
            logger.error(f"❌ Erreur envoi message WhatsApp: {str(e)}")
            return False
    
    def send_document(self, to_number: str, file_url: str, caption: str = "") -> bool:
        """Envoie un document WhatsApp via Twilio."""
        try:
            if not self.client:
                logger.info(f"📎 [SIMULÉ] Document WhatsApp à {to_number}: {file_url}")
                return True
            
            # Normaliser le numéro
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            # Envoyer le document
            message_instance = self.client.messages.create(
                body=caption,
                media_url=[file_url],
                from_=self.whatsapp_number,
                to=to_number
            )
            
            logger.info(f"✅ Document WhatsApp envoyé - SID: {message_instance.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"❌ Erreur Twilio document: {e.msg} (Code: {e.code})")
            
            # Gérer spécifiquement la limite quotidienne
            if e.code == 63038:
                logger.warning("📊 Limite quotidienne Twilio atteinte - Mode simulation activé")
                logger.info(f"📎 [SIMULÉ - LIMITE] Document WhatsApp à {to_number}: {file_url}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"❌ Erreur envoi document WhatsApp: {str(e)}")
            return False
    
    def send_business_plan_files(self, to_number: str, excel_url: str, pdf_url: str, business_plan_title: str) -> bool:
        """Envoie les fichiers de business plan via WhatsApp."""
        try:
            success = True
            
            # Vérifier si les URLs sont accessibles publiquement
            if not excel_url.startswith('http'):
                logger.warning(f"⚠️ URL Excel non publique: {excel_url}")
                # Envoyer un message informatif au lieu du fichier
                info_message = f"📊 Business Plan Excel: {business_plan_title}\n💾 Téléchargez depuis: {excel_url}"
                if not self.send_message(to_number, info_message):
                    success = False
            else:
                # Envoyer le fichier Excel (Business Plan)
                excel_caption = f"📊 Business Plan Excel: {business_plan_title}"
                if not self.send_document(to_number, excel_url, excel_caption):
                    success = False
            
            if not pdf_url.startswith('http'):
                logger.warning(f"⚠️ URL PDF non publique: {pdf_url}")
                # Envoyer un message informatif au lieu du fichier
                info_message = f"🔧 Itinéraire Technique PDF: {business_plan_title}\n💾 Téléchargez depuis: {pdf_url}"
                if not self.send_message(to_number, info_message):
                    success = False
            else:
                # Envoyer le fichier PDF (Itinéraire Technique)
                pdf_caption = f"🔧 Itinéraire Technique PDF: {business_plan_title}"
                if not self.send_document(to_number, pdf_url, pdf_caption):
                    success = False
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi fichiers business plan: {str(e)}")
            return False
    
    def send_simple_message(self, to_number: str, message: str) -> bool:
        """Envoie un message simple."""
        return self.send_message(to_number, message)
    
    def send_welcome_message(self, to_number: str, user_request: str) -> bool:
        """Envoie le message de bienvenue."""
        welcome_message = f"""

📝 *Votre demande:* {user_request}

⏳ Je vais analyser tous les documents de notre base de données et créer un business plan complet personnalisé pour votre projet de culture de maïs...

📊 Génération en cours des fichiers Excel et PDF..."""
        
        return self.send_message(to_number, welcome_message)
    
    def send_success_message(self, to_number: str, business_plan: dict, files: dict, documents_analyzed: int, download_base_url: str) -> bool:
        """Envoie le message de succès avec les détails du business plan."""
        
        resume = business_plan.get('resume_executif', {}).get('description_projet', 'Plan d\'affaires détaillé basé sur votre demande')
        if len(resume) > 200:
            resume = resume[:200] + "..."
        
        # S'assurer que l'URL de base n'a pas de slash à la fin
        base_url = download_base_url.rstrip('/')
        
        # Construire les URLs complètes
        excel_url = f"{base_url}/api/gemini/download/{files['excel']['filename']}"
        pdf_url = f"{base_url}/api/gemini/download/{files['pdf']['filename']}"
        
        success_message = f"""✅ *Business Plan Maïs généré avec succès !*

📋 *Titre:* {business_plan.get('titre', 'Business Plan Maïs Personnalisé')}

📈 *Résumé:* {resume[:150]}...

📊 *Documents analysés:* {documents_analyzed}

📁 *Fichiers générés:*
• 📊 Business Plan Excel: {files['excel']['filename']}
• 🔧 Itinéraire Technique PDF: {files['pdf']['filename']}

💾 *Téléchargement:*
• Business Plan: {excel_url}
• Itinéraire Technique: {pdf_url}

🎯 *Inclus:* Analyse marché, stratégie marketing, projections financières, plan opérationnel

🔧 *Technique:* Architecture, spécifications, planning, stack technologique

🌽 *Spécialisé maïs uniquement*

📱 Fichiers envoyés dans ce chat."""
        
        # Envoyer le message
        if not self.send_message(to_number, success_message):
            return False
        
        # Envoyer les fichiers
        return self.send_business_plan_files(
            to_number, 
            excel_url, 
            pdf_url, 
            business_plan.get('titre', 'Business Plan')
        )
    
    def send_error_message(self, to_number: str, error: str, is_rate_limited: bool = False) -> bool:
        """Envoie un message d'erreur."""
        if is_rate_limited:
            error_message = f"""🚫 *Limite d'utilisation atteinte*

{error}

🔓 *Pour continuer à utiliser le service:*
• Envoyez le code d'accès: `**********`
• Ce code vous débloquera pour un accès illimité

📊 *Votre utilisation actuelle:*
• Vous avez utilisé 5 requêtes gratuites
• Après le déblocage, vous pourrez faire des requêtes illimitées

💡 *Le code d'accès est:* `**********`"""
        else:
            error_message = f"""❌ *Erreur lors de la génération*

Je n'ai pas pu créer votre business plan.
*Erreur:* {error}

🔄 Veuillez réessayer avec une description plus détaillée de votre projet de culture de maïs.

💡 *Conseils pour améliorer votre demande:*
• Décrivez clairement votre projet de culture de maïs
• Mentionnez la superficie (ex: 10 ha, 5 hectares)
• Précisez le type de maïs (grain, fourrage, doux)
• Indiquez vos besoins en irrigation ou fertilisation

🌽 *Exemples de demandes valides pour maïs:*
• "Je veux faire du maïs sur 10 ha"
• "Culture de maïs grain avec irrigation"
• "Production de maïs fourrage sur 5 hectares"

⚠️ *ATTENTION : Je suis spécialisé uniquement sur la culture de maïs*

📞 Pour un support technique, contactez notre équipe."""
        
        return self.send_message(to_number, error_message)
    
    def send_system_error_message(self, to_number: str) -> bool:
        """Envoie un message d'erreur système."""
        system_error_message = """🚨 *Erreur système temporaire*

Notre service rencontre actuellement des difficultés techniques.

⏰ Veuillez réessayer dans quelques minutes.

🛠️ Notre équipe technique a été notifiée automatiquement.

📧 En cas de problème persistant, contactez-nous à support@votre-domaine.com"""
        
        return self.send_message(to_number, system_error_message)
    
    def send_unlock_message(self, to_number: str, success: bool, message: str) -> bool:
        """Envoie un message de déblocage."""
        if success:
            unlock_message = f"""✅ *Compte débloqué avec succès !*

{message}

🎉 *Vous pouvez maintenant:*
• Faire des requêtes illimitées
• Générer autant de business plans que vous voulez
• Accéder à toutes les fonctionnalités

🚀 *Envoyez votre prochaine demande de business plan pour maïs !*"""
        else:
            unlock_message = f"""❌ *Échec du déblocage*

{message}

🔑 *Vérifiez que vous avez bien envoyé:* `**********`

💡 *Le code doit être exactement:* `**********`"""
        
        return self.send_message(to_number, unlock_message)
    
    def get_webhook_validation_token(self) -> Optional[str]:
        """Retourne le token de validation pour les webhooks WhatsApp."""
        return os.getenv('WHATSAPP_WEBHOOK_VERIFY_TOKEN', 'your_verify_token_here')
    
    def validate_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """Valide un webhook WhatsApp."""
        verify_token = self.get_webhook_validation_token()
        
        if mode == "subscribe" and token == verify_token:
            logger.info("✅ Webhook WhatsApp validé avec succès")
            return challenge
        else:
            logger.warning(f"❌ Échec validation webhook - mode: {mode}, token: {token}")
            return None

# Instance globale du service
whatsapp_service = WhatsAppService() 