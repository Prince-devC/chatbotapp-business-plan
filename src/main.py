import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from pathlib import Path

from src.models.database import db
from src.routes.admin import admin_bp
from src.routes.chatbot import chatbot_bp
from src.routes.business_plan import business_plan_bp
from src.routes.user import user_bp
from src.routes.gemini import gemini_bp

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')

# Configuration de la base de données
basedir = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(basedir, '..', 'database', 'app.db')
project_root = Path(__file__).parent.parent.resolve()
db_dir = project_root / 'database'
db_path = db_dir / 'app.db'

print(f"Base directory: {project_root}")
print(f"Database path: {db_path}")
print(f"Current working directory: {os.getcwd()}")

# S'assurer que le répertoire parent existe
db_dir.mkdir(parents=True, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration JWT - S'assurer que l'identité est gérée de manière cohérente
app.config['JWT_IDENTITY_CLAIM'] = 'user_id'

# Configuration des uploads de fichiers
UPLOAD_FOLDER = os.path.join(project_root, 'uploads', 'templates')
ALLOWED_EXTENSIONS = {'pdf', 'xls', 'xlsx', 'doc', 'docx', 'png', 'webp', 'jpg', 'jpeg', 'txt'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Ensure the upload directory exists

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Initialisation des extensions
CORS(app, origins="*")  # Permettre toutes les origines pour le développement
jwt = JWTManager(app)
print(f"SQLALCHEMY_DATABASE_URI before init_app: {app.config['SQLALCHEMY_DATABASE_URI']}")
db.init_app(app)
migrate = Migrate(app, db)

# Enregistrement des blueprints
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(business_plan_bp, url_prefix='/api/business-plan')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(gemini_bp, url_prefix='/api/gemini')

# Routes alternatives pour les webhooks (sans le préfixe /api/chatbot)
from src.routes.chatbot import whatsapp_webhook, telegram_webhook, messenger_webhook, whatsapp_gemini_webhook
app.add_url_rule('/webhook/whatsapp', 'whatsapp_webhook_root', whatsapp_webhook, methods=['POST'])
app.add_url_rule('/webhook/whatsapp-gemini', 'whatsapp_gemini_webhook_root', whatsapp_gemini_webhook, methods=['POST'])
app.add_url_rule('/webhook/telegram', 'telegram_webhook_root', telegram_webhook, methods=['POST'])
app.add_url_rule('/webhook/messenger', 'messenger_webhook_root', messenger_webhook, methods=['POST'])

# Création des tables
with app.app_context():
    print(f"Attempting to create all tables for URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        import traceback
        traceback.print_exc()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'chatbot-business-plan'}, 200

@app.route('/uploads/templates/<filename>')
def uploaded_file(filename):
    """Servir les fichiers uploadés"""
    upload_folder = app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)

@app.route('/download/<filename>')
def download_generated_file(filename):
    """Servir les business plans générés"""
    try:
        # Utiliser le chemin absolu vers le dossier de génération
        generated_dir = os.path.join(project_root, 'generated_business_plans')
        file_path = os.path.join(generated_dir, filename)
        
        print(f"Tentative téléchargement: {file_path}")
        print(f"Fichier existe: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            print(f"Fichier non trouvé: {file_path}")
            return "Fichier non trouvé", 404
        
        # Déterminer le type MIME
        if filename.endswith('.xlsx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif filename.endswith('.pdf'):
            mimetype = 'application/pdf'
        else:
            mimetype = 'application/octet-stream'
        
        print(f"Servir fichier depuis: {generated_dir}")
        return send_from_directory(generated_dir, filename, mimetype=mimetype, as_attachment=True)
        
    except Exception as e:
        print(f"Erreur téléchargement {filename}: {str(e)}")
        import traceback
        traceback.print_exc()
        return "Erreur lors du téléchargement", 500

if __name__ == '__main__':
    # Port pour la production (Railway, Heroku, etc.)
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)

