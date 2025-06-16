import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from src.models.database import db
from src.routes.admin import admin_bp
from src.routes.chatbot import chatbot_bp
from src.routes.business_plan import business_plan_bp

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')

# Configuration de la base de données
database_url = os.getenv('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Utiliser un chemin absolu cohérent
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'app.db')
    
    print(f"Base directory: {basedir}")
    print(f"Database path: {db_path}")
    print(f"Current working directory: {os.getcwd()}")
    
    # S'assurer que le répertoire parent existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
CORS(app, origins="*")  # Permettre toutes les origines pour le développement
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

# Enregistrement des blueprints
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(business_plan_bp, url_prefix='/api/business-plan')

# Routes alternatives pour les webhooks (sans le préfixe /api/chatbot)
from src.routes.chatbot import whatsapp_webhook, telegram_webhook, messenger_webhook
app.add_url_rule('/webhook/whatsapp', 'whatsapp_webhook_root', whatsapp_webhook, methods=['POST'])
app.add_url_rule('/webhook/telegram', 'telegram_webhook_root', telegram_webhook, methods=['POST'])
app.add_url_rule('/webhook/messenger', 'messenger_webhook_root', messenger_webhook, methods=['POST'])

# Création des tables
with app.app_context():
    db.create_all()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

