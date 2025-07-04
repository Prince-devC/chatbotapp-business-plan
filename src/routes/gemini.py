from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
import os
import logging
from datetime import datetime
from pathlib import Path
from src.services.gemini_service import GeminiAnalysisService
from src.services.document_generator import DocumentGenerator
from src.models.database import get_db_connection

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

gemini_bp = Blueprint('gemini', __name__)

@gemini_bp.route('/analyze-and-generate', methods=['POST'])
@jwt_required()
def analyze_and_generate_business_plan():
    """
    Analyse tous les documents de la base de données avec Gemini
    et génère un business plan complet Excel + PDF
    """
    try:
        data = request.get_json()
        user_request = data.get('user_request', '')
        generate_excel = data.get('generate_excel', True)
        generate_pdf = data.get('generate_pdf', True)
        
        if not user_request:
            return jsonify({
                'success': False,
                'error': 'user_request est requis'
            }), 400
        
        # Récupérer tous les templates de la base de données
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, category, file_path, file_type, uploaded_at
            FROM business_plan_templates
            ORDER BY uploaded_at DESC
        """)
        
        templates = []
        for row in cursor.fetchall():
            templates.append({
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'file_path': row[3],
                'file_type': row[4],
                'uploaded_at': row[5]
            })
        
        conn.close()
        
        if not templates:
            return jsonify({
                'success': False,
                'error': 'Aucun template disponible dans la base de données'
            }), 404
        
        # Initialiser le service Gemini
        gemini_service = GeminiAnalysisService()
        
        # Analyser les documents avec Gemini
        logger.info(f"Début de l'analyse de {len(templates)} documents avec Gemini")
        analysis_result = gemini_service.analyze_documents_for_business_plan(templates, user_request)
        
        if not analysis_result['success']:
            return jsonify({
                'success': False,
                'error': f"Erreur lors de l'analyse Gemini: {analysis_result.get('error')}",
                'documents_analyzed': analysis_result.get('documents_analyzed', 0)
            }), 500
        
        business_plan_data = analysis_result['business_plan']
        
        # Initialiser le générateur de documents
        doc_generator = DocumentGenerator()
        
        generated_files = []
        
        # Générer Excel si demandé
        if generate_excel:
            try:
                excel_filename = f"business_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                excel_path = doc_generator.generate_excel_business_plan(business_plan_data, excel_filename)
                generated_files.append({
                    'type': 'excel',
                    'filename': excel_filename,
                    'path': excel_path,
                    'download_url': f'/api/gemini/download/{excel_filename}'
                })
                logger.info(f"Fichier Excel généré: {excel_path}")
            except Exception as e:
                logger.error(f"Erreur génération Excel: {str(e)}")
        
        # Générer PDF si demandé
        if generate_pdf:
            try:
                pdf_filename = f"business_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf_path = doc_generator.generate_pdf_business_plan(business_plan_data, pdf_filename)
                generated_files.append({
                    'type': 'pdf',
                    'filename': pdf_filename,
                    'path': pdf_path,
                    'download_url': f'/api/gemini/download/{pdf_filename}'
                })
                logger.info(f"Fichier PDF généré: {pdf_path}")
            except Exception as e:
                logger.error(f"Erreur génération PDF: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': 'Business plan généré avec succès',
            'business_plan': business_plan_data,
            'generated_files': generated_files,
            'documents_analyzed': analysis_result['documents_analyzed'],
            'user_request': user_request,
            'analysis_timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur dans analyze_and_generate_business_plan: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur interne du serveur: {str(e)}'
        }), 500

@gemini_bp.route('/whatsapp-webhook', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook pour recevoir les messages WhatsApp et générer automatiquement
    des business plans
    """
    try:
        data = request.get_json()
        
        # Extraire le message WhatsApp (format dépend du provider)
        message = data.get('message', {}).get('text', '')
        phone_number = data.get('from', '')
        
        if not message:
            return jsonify({'status': 'no_message'}), 200
        
        logger.info(f"Message WhatsApp reçu de {phone_number}: {message}")
        
        # Récupérer tous les templates
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, category, file_path, file_type
            FROM business_plan_templates
        """)
        
        templates = []
        for row in cursor.fetchall():
            templates.append({
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'file_path': row[3],
                'file_type': row[4]
            })
        
        conn.close()
        
        if templates:
            # Analyser avec Gemini
            gemini_service = GeminiAnalysisService()
            result = gemini_service.analyze_documents_for_business_plan(templates, message)
            
            if result['success']:
                # Générer les fichiers
                doc_generator = DocumentGenerator()
                
                # Générer Excel et PDF
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                excel_path = doc_generator.generate_excel_business_plan(
                    result['business_plan'], 
                    f"business_plan_whatsapp_{timestamp}.xlsx"
                )
                pdf_path = doc_generator.generate_pdf_business_plan(
                    result['business_plan'], 
                    f"business_plan_whatsapp_{timestamp}.pdf"
                )
                
                logger.info(f"Business plan généré pour WhatsApp {phone_number}")
                
                return jsonify({
                    'status': 'success',
                    'message': 'Business plan généré',
                    'excel_path': excel_path,
                    'pdf_path': pdf_path
                }), 200
        
        return jsonify({'status': 'processed'}), 200
        
    except Exception as e:
        logger.error(f"Erreur webhook WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@gemini_bp.route('/download/<filename>')
@jwt_required()
def download_generated_file(filename):
    """Télécharge un fichier généré"""
    try:
        # Utiliser le chemin absolu
        project_root = Path(__file__).parent.parent.parent.resolve()
        file_path = os.path.join(project_root, 'generated_business_plans', filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Fichier non trouvé'}), 404
        
        if filename.endswith('.xlsx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif filename.endswith('.pdf'):
            mimetype = 'application/pdf'
        else:
            mimetype = 'application/octet-stream'
        
        return send_file(file_path, mimetype=mimetype, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"Erreur téléchargement {filename}: {str(e)}")
        return jsonify({'error': 'Erreur lors du téléchargement'}), 500
