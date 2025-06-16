from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class AIConfiguration(db.Model):
    __tablename__ = 'ai_configurations'
    
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)  # 'openai', 'claude', 'gemini'
    api_key_encrypted = db.Column(db.Text, nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    max_tokens = db.Column(db.Integer, default=4000)
    temperature = db.Column(db.Float, default=0.7)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'provider': self.provider,
            'model_name': self.model_name,
            'is_active': self.is_active,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class BusinessPlanTemplate(db.Model):
    __tablename__ = 'business_plan_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    template_content = db.Column(db.Text, nullable=False)  # JSON ou HTML template
    variables = db.Column(db.Text)  # JSON - Liste des variables requises
    category = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    creator = db.relationship('AdminUser', backref='templates')
    
    def get_variables(self):
        if self.variables:
            try:
                return json.loads(self.variables)
            except:
                return []
        return []
    
    def set_variables(self, variables_list):
        self.variables = json.dumps(variables_list)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template_content': self.template_content,
            'variables': self.get_variables(),
            'category': self.category,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CompanyData(db.Model):
    __tablename__ = 'company_data'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100))
    size = db.Column(db.String(50))  # 'startup', 'small', 'medium', 'large'
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    financial_data = db.Column(db.Text)  # JSON - Données financières structurées
    market_data = db.Column(db.Text)  # JSON - Données de marché
    competitive_data = db.Column(db.Text)  # JSON - Données concurrentielles
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_financial_data(self):
        if self.financial_data:
            try:
                return json.loads(self.financial_data)
            except:
                return {}
        return {}
    
    def set_financial_data(self, data):
        self.financial_data = json.dumps(data)
    
    def get_market_data(self):
        if self.market_data:
            try:
                return json.loads(self.market_data)
            except:
                return {}
        return {}
    
    def set_market_data(self, data):
        self.market_data = json.dumps(data)
    
    def get_competitive_data(self):
        if self.competitive_data:
            try:
                return json.loads(self.competitive_data)
            except:
                return {}
        return {}
    
    def set_competitive_data(self, data):
        self.competitive_data = json.dumps(data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'industry': self.industry,
            'size': self.size,
            'location': self.location,
            'description': self.description,
            'financial_data': self.get_financial_data(),
            'market_data': self.get_market_data(),
            'competitive_data': self.get_competitive_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)  # 'whatsapp', 'telegram', 'messenger'
    platform_user_id = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    language_code = db.Column(db.String(10), default='fr')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_interaction = db.Column(db.DateTime)
    
    # Contrainte d'unicité
    __table_args__ = (db.UniqueConstraint('platform', 'platform_user_id'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'platform_user_id': self.platform_user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'language_code': self.language_code,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None
        }

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'abandoned'
    context = db.Column(db.Text)  # JSON - Contexte de la conversation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='conversations')
    
    def get_context(self):
        if self.context:
            try:
                return json.loads(self.context)
            except:
                return {}
        return {}
    
    def set_context(self, context_data):
        self.context = json.dumps(context_data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'status': self.status,
            'context': self.get_context(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' ou 'bot'
    message_type = db.Column(db.String(20), default='text')  # 'text', 'image', 'document', 'audio'
    content = db.Column(db.Text, nullable=False)
    metadata_info = db.Column(db.Text)  # JSON - Données supplémentaires
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    conversation = db.relationship('Conversation', backref='messages')
    
    def get_metadata(self):
        if self.metadata_info:
            try:
                return json.loads(self.metadata_info)
            except:
                return {}
        return {}
    
    def set_metadata(self, metadata_data):
        self.metadata_info = json.dumps(metadata_data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender': self.sender,
            'message_type': self.message_type,
            'content': self.content,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BusinessPlan(db.Model):
    __tablename__ = 'business_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('business_plan_templates.id'))
    company_name = db.Column(db.String(200), nullable=False)
    generated_content = db.Column(db.Text, nullable=False)
    variables_used = db.Column(db.Text)  # JSON - Variables utilisées pour la génération
    file_path = db.Column(db.String(500))  # Chemin vers le fichier généré
    file_format = db.Column(db.String(10), default='pdf')  # 'pdf', 'docx', 'html'
    status = db.Column(db.String(20), default='generated')  # 'generated', 'sent', 'downloaded'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='business_plans')
    conversation = db.relationship('Conversation', backref='business_plans')
    template = db.relationship('BusinessPlanTemplate', backref='business_plans')
    
    def get_variables_used(self):
        if self.variables_used:
            try:
                return json.loads(self.variables_used)
            except:
                return {}
        return {}
    
    def set_variables_used(self, variables_data):
        self.variables_used = json.dumps(variables_data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'conversation_id': self.conversation_id,
            'template_id': self.template_id,
            'company_name': self.company_name,
            'generated_content': self.generated_content,
            'variables_used': self.get_variables_used(),
            'file_path': self.file_path,
            'file_format': self.file_format,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AIInteraction(db.Model):
    __tablename__ = 'ai_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    ai_provider = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    tokens_used = db.Column(db.Integer)
    cost = db.Column(db.Float)  # Coût de l'interaction
    response_time = db.Column(db.Integer)  # Temps de réponse en ms
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    conversation = db.relationship('Conversation', backref='ai_interactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'ai_provider': self.ai_provider,
            'prompt': self.prompt,
            'response': self.response,
            'tokens_used': self.tokens_used,
            'cost': self.cost,
            'response_time': self.response_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class WebhookLog(db.Model):
    __tablename__ = 'webhook_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)
    webhook_data = db.Column(db.Text, nullable=False)  # JSON
    processed = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_webhook_data(self):
        if self.webhook_data:
            try:
                return json.loads(self.webhook_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_webhook_data(self, data):
        try:
            self.webhook_data = json.dumps(data, ensure_ascii=False)
        except Exception as e:
            self.webhook_data = json.dumps({'error': str(e)})
    
    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'webhook_data': self.get_webhook_data(),
            'processed': self.processed,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

