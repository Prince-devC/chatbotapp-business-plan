from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os
from werkzeug.utils import secure_filename
from flask import current_app # To access app.config
import json

from src.models.database import db, AdminUser, AIConfiguration, BusinessPlanTemplate, CompanyData

admin_bp = Blueprint('admin', __name__)

# Clé de chiffrement pour les clés API (à stocker en variable d'environnement)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY)

@admin_bp.route('/login', methods=['POST'])
def login():
    """Connexion administrateur"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username et password requis'}), 400
    
    admin = AdminUser.query.filter_by(username=username, is_active=True).first()
    
    if admin and check_password_hash(admin.password_hash, password):
        # Mise à jour de la dernière connexion
        admin.last_login = datetime.utcnow()
        db.session.commit()
        
        # Création du token JWT avec une identité structurée
        identity = {'user_id': admin.id, 'username': admin.username}
        access_token = create_access_token(
            identity=identity,
            expires_delta=timedelta(hours=24)
        )
        
        return jsonify({
            'access_token': access_token,
            'admin': admin.to_dict()
        }), 200
    
    return jsonify({'error': 'Identifiants invalides'}), 401

@admin_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    """Création d'un nouvel administrateur (réservé aux admins existants)"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Tous les champs sont requis'}), 400
    
    # Vérifier si l'utilisateur existe déjà
    if AdminUser.query.filter_by(username=username).first():
        return jsonify({'error': 'Username déjà utilisé'}), 400
    
    if AdminUser.query.filter_by(email=email).first():
        return jsonify({'error': 'Email déjà utilisé'}), 400
    
    # Créer le nouvel administrateur
    admin = AdminUser(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    
    db.session.add(admin)
    db.session.commit()
    
    return jsonify({'message': 'Administrateur créé avec succès', 'admin': admin.to_dict()}), 201

@admin_bp.route('/ai-configurations', methods=['GET'])
@jwt_required()
def get_ai_configurations():
    """Récupérer toutes les configurations IA"""
    configs = AIConfiguration.query.all()
    return jsonify([config.to_dict() for config in configs]), 200

@admin_bp.route('/ai-configurations', methods=['POST'])
@jwt_required()
def create_ai_configuration():
    """Créer une nouvelle configuration IA"""
    data = request.get_json()
    
    required_fields = ['provider', 'api_key', 'model_name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs requis: provider, api_key, model_name'}), 400
    
    # Chiffrer la clé API
    encrypted_key = cipher_suite.encrypt(data['api_key'].encode()).decode()
    
    config = AIConfiguration(
        provider=data['provider'],
        api_key_encrypted=encrypted_key,
        model_name=data['model_name'],
        max_tokens=data.get('max_tokens', 4000),
        temperature=data.get('temperature', 0.7)
    )
    
    db.session.add(config)
    db.session.commit()
    
    return jsonify({'message': 'Configuration IA créée', 'config': config.to_dict()}), 201

@admin_bp.route('/ai-configurations/<int:config_id>', methods=['PUT'])
@jwt_required()
def update_ai_configuration(config_id):
    """Mettre à jour une configuration IA"""
    config = AIConfiguration.query.get_or_404(config_id)
    data = request.get_json()
    
    if 'api_key' in data:
        config.api_key_encrypted = cipher_suite.encrypt(data['api_key'].encode()).decode()
    
    if 'model_name' in data:
        config.model_name = data['model_name']
    if 'max_tokens' in data:
        config.max_tokens = data['max_tokens']
    if 'temperature' in data:
        config.temperature = data['temperature']
    if 'is_active' in data:
        config.is_active = data['is_active']
    
    config.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Configuration mise à jour', 'config': config.to_dict()}), 200

@admin_bp.route('/business-plan-templates', methods=['GET'])
@jwt_required()
def get_business_plan_templates():
    """Récupérer tous les templates de business plans"""
    templates = BusinessPlanTemplate.query.all()
    return jsonify([template.to_dict() for template in templates]), 200

@admin_bp.route('/business-plan-templates', methods=['POST'])
@jwt_required()
def create_business_plan_template():
    """Créer un nouveau template de business plan"""
    jwt_identity = get_jwt_identity()
    admin_id = jwt_identity.get('user_id')
    
    if not admin_id:
        return jsonify({'error': 'Identité administrateur invalide dans le token'}), 401
        
    data = request.get_json()
    
    required_fields = ['name', 'template_content']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs requis: name, template_content'}), 400
    
    template = BusinessPlanTemplate(
        name=data['name'],
        description=data.get('description'),
        template_content=data['template_content'],
        category=data.get('category'),
        created_by=admin_id
    )
    
    if 'variables' in data:
        template.set_variables(data['variables'])
    
    db.session.add(template)
    db.session.commit()
    
    return jsonify({'message': 'Template créé', 'template': template.to_dict()}), 201

@admin_bp.route('/business-plan-templates/<int:template_id>', methods=['PUT'])
@jwt_required()
def update_business_plan_template(template_id):
    """Mettre à jour un template de business plan"""
    template = BusinessPlanTemplate.query.get_or_404(template_id)
    data = request.get_json()
    
    if 'name' in data:
        template.name = data['name']
    if 'description' in data:
        template.description = data['description']
    if 'template_content' in data:
        template.template_content = data['template_content']
    if 'category' in data:
        template.category = data['category']
    if 'variables' in data:
        template.set_variables(data['variables'])
    if 'is_active' in data:
        template.is_active = data['is_active']
    
    template.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Template mis à jour', 'template': template.to_dict()}), 200

@admin_bp.route('/business-plan-templates/upload', methods=['POST'])
@jwt_required()
def upload_business_plan_template():
    """Uploader un nouveau template de business plan"""
    
    def allowed_file(filename):
        """Vérifie si l'extension du fichier est autorisée."""
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS')
        if not allowed_extensions:
            # Fallback au cas où la configuration ne serait pas chargée, même si c'est peu probable ici.
            allowed_extensions = {'pdf', 'xls', 'xlsx', 'doc', 'docx', 'png', 'webp', 'jpg', 'jpeg', 'txt'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    try:
        jwt_identity = get_jwt_identity()
        admin_id = jwt_identity.get('user_id')
        
        if not admin_id:
            return jsonify({'error': 'Identité administrateur invalide dans le token'}), 401

        print(f"Admin ID: {admin_id}")
        print(f"Request form: {request.form}")
        print(f"Request files: {request.files}")

        if 'file' not in request.files:
            print("Erreur: Aucun fichier fourni")
            return jsonify({'error': 'Aucun fichier fourni'}), 400

        file = request.files['file']
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        variables = request.form.get('variables') # JSON string

        print(f"Nom: {name}")
        print(f"Description: {description}")
        print(f"Catégorie: {category}")
        print(f"Variables: {variables}")
        print(f"Nom du fichier: {file.filename}")

        if file.filename == '':
            print("Erreur: Aucun fichier sélectionné")
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
            
        if not name:
            print("Erreur: Le nom du template est requis")
            return jsonify({'error': 'Le nom du template est requis'}), 422

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            print(f"Chemin du fichier: {file_path}")
            file.save(file_path)

            # Déterminer le type de fichier (extension)
            file_type = filename.rsplit('.', 1)[1].lower()
            print(f"Type de fichier: {file_type}")

            template = BusinessPlanTemplate(
                name=name,
                description=description,
                file_path=file_path,
                file_type=file_type,
                category=category,
                created_by=admin_id
            )

            if variables:
                try:
                    template.set_variables(json.loads(variables))
                except json.JSONDecodeError:
                    print("Erreur: Format de variables invalide")
                    return jsonify({'error': 'Format de variables invalide. Doit être un JSON valide.'}), 400

            db.session.add(template)
            db.session.commit()
            print("Template ajouté avec succès à la base de données")

            return jsonify({'message': 'Template de business plan uploadé avec succès', 'template': template.to_dict()}), 201
        else:
            allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', [])
            print(f"Erreur: Type de fichier non autorisé. Extensions autorisées: {allowed_extensions}")
            return jsonify({'error': f'Type de fichier non autorisé. Extensions autorisées: {allowed_extensions}'}), 400
    except Exception as e:
        print(f"Exception lors de l'upload: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@admin_bp.route('/business-plan-templates/public', methods=['GET'])
def get_public_business_plan_templates():
    """Récupérer tous les templates de business plans (route publique)"""
    templates = BusinessPlanTemplate.query.filter_by(is_active=True).all()
    return jsonify([template.to_dict() for template in templates]), 200

@admin_bp.route('/company-data', methods=['GET'])
@jwt_required()
def get_company_data():
    """Récupérer toutes les données d'entreprises"""
    companies = CompanyData.query.all()
    return jsonify([company.to_dict() for company in companies]), 200

@admin_bp.route('/company-data', methods=['POST'])
@jwt_required()
def create_company_data():
    """Créer de nouvelles données d'entreprise"""
    data = request.get_json()
    
    if not data.get('company_name'):
        return jsonify({'error': 'Nom de l\'entreprise requis'}), 400
    
    company = CompanyData(
        company_name=data['company_name'],
        industry=data.get('industry'),
        size=data.get('size'),
        location=data.get('location'),
        description=data.get('description')
    )
    
    if 'financial_data' in data:
        company.set_financial_data(data['financial_data'])
    if 'market_data' in data:
        company.set_market_data(data['market_data'])
    if 'competitive_data' in data:
        company.set_competitive_data(data['competitive_data'])
    
    db.session.add(company)
    db.session.commit()
    
    return jsonify({'message': 'Données d\'entreprise créées', 'company': company.to_dict()}), 201

@admin_bp.route('/company-data/<int:company_id>', methods=['PUT'])
@jwt_required()
def update_company_data(company_id):
    """Mettre à jour les données d'une entreprise"""
    company = CompanyData.query.get_or_404(company_id)
    data = request.get_json()
    
    if 'company_name' in data:
        company.company_name = data['company_name']
    if 'industry' in data:
        company.industry = data['industry']
    if 'size' in data:
        company.size = data['size']
    if 'location' in data:
        company.location = data['location']
    if 'description' in data:
        company.description = data['description']
    if 'financial_data' in data:
        company.set_financial_data(data['financial_data'])
    if 'market_data' in data:
        company.set_market_data(data['market_data'])
    if 'competitive_data' in data:
        company.set_competitive_data(data['competitive_data'])
    
    company.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Données d\'entreprise mises à jour', 'company': company.to_dict()}), 200

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Récupérer les statistiques du système"""
    from src.models.database import User, Conversation, BusinessPlan, Message
    
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'total_conversations': Conversation.query.count(),
        'active_conversations': Conversation.query.filter_by(status='active').count(),
        'total_business_plans': BusinessPlan.query.count(),
        'total_messages': Message.query.count(),
        'total_templates': BusinessPlanTemplate.query.count(),
        'active_templates': BusinessPlanTemplate.query.filter_by(is_active=True).count(),
        'total_companies': CompanyData.query.count(),
        'ai_configurations': AIConfiguration.query.filter_by(is_active=True).count()
    }
    
    return jsonify(stats), 200

