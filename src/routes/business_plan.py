from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
import os
import json

from src.models.database import db, BusinessPlan, BusinessPlanTemplate, User, Conversation, CompanyData

business_plan_bp = Blueprint('business_plan', __name__)

@business_plan_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_business_plan():
    """Générer un business plan"""
    data = request.get_json()
    
    required_fields = ['template_id', 'company_name', 'variables']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs requis: template_id, company_name, variables'}), 400
    
    # Récupérer le template
    template = BusinessPlanTemplate.query.get_or_404(data['template_id'])
    if not template.is_active:
        return jsonify({'error': 'Template non actif'}), 400
    
    # Générer le contenu du business plan
    try:
        generated_content = generate_business_plan_content(
            template.template_content,
            data['variables'],
            data['company_name']
        )
        
        # Créer l'enregistrement du business plan
        business_plan = BusinessPlan(
            user_id=data.get('user_id'),
            conversation_id=data.get('conversation_id'),
            template_id=template.id,
            company_name=data['company_name'],
            generated_content=generated_content
        )
        business_plan.set_variables_used(data['variables'])
        
        db.session.add(business_plan)
        db.session.commit()
        
        return jsonify({
            'message': 'Business plan généré avec succès',
            'business_plan': business_plan.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la génération: {str(e)}'}), 500

@business_plan_bp.route('/export/<int:business_plan_id>', methods=['POST'])
@jwt_required()
def export_business_plan(business_plan_id):
    """Exporter un business plan en PDF ou autre format"""
    business_plan = BusinessPlan.query.get_or_404(business_plan_id)
    data = request.get_json()
    
    export_format = data.get('format', 'pdf')
    
    try:
        file_path = export_business_plan_to_file(
            business_plan.generated_content,
            business_plan.company_name,
            export_format
        )
        
        # Mettre à jour le business plan avec le chemin du fichier
        business_plan.file_path = file_path
        business_plan.file_format = export_format
        db.session.commit()
        
        return jsonify({
            'message': 'Business plan exporté avec succès',
            'file_path': file_path,
            'download_url': f'/api/business-plan/download/{business_plan_id}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de l\'export: {str(e)}'}), 500

@business_plan_bp.route('/download/<int:business_plan_id>')
def download_business_plan(business_plan_id):
    """Télécharger un business plan exporté"""
    business_plan = BusinessPlan.query.get_or_404(business_plan_id)
    
    if not business_plan.file_path or not os.path.exists(business_plan.file_path):
        return jsonify({'error': 'Fichier non trouvé'}), 404
    
    from flask import send_file
    return send_file(
        business_plan.file_path,
        as_attachment=True,
        download_name=f"{business_plan.company_name}_business_plan.{business_plan.file_format}"
    )

@business_plan_bp.route('/list', methods=['GET'])
@jwt_required()
def list_business_plans():
    """Lister les business plans générés"""
    user_id = request.args.get('user_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    query = BusinessPlan.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    business_plans = query.order_by(BusinessPlan.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'business_plans': [bp.to_dict() for bp in business_plans.items],
        'total': business_plans.total,
        'pages': business_plans.pages,
        'current_page': page
    }), 200

@business_plan_bp.route('/<int:business_plan_id>', methods=['GET'])
@jwt_required()
def get_business_plan(business_plan_id):
    """Récupérer un business plan spécifique"""
    business_plan = BusinessPlan.query.get_or_404(business_plan_id)
    return jsonify(business_plan.to_dict()), 200

@business_plan_bp.route('/templates/variables/<int:template_id>', methods=['GET'])
def get_template_variables(template_id):
    """Récupérer les variables requises pour un template"""
    template = BusinessPlanTemplate.query.get_or_404(template_id)
    
    if not template.is_active:
        return jsonify({'error': 'Template non actif'}), 400
    
    return jsonify({
        'template_id': template.id,
        'template_name': template.name,
        'variables': template.get_variables(),
        'description': template.description
    }), 200

@business_plan_bp.route('/suggest-data', methods=['POST'])
def suggest_company_data():
    """Suggérer des données d'entreprise basées sur le nom ou l'industrie"""
    data = request.get_json()
    company_name = data.get('company_name', '').strip()
    industry = data.get('industry', '').strip()
    
    suggestions = []
    
    # Rechercher par nom d'entreprise
    if company_name:
        companies = CompanyData.query.filter(
            CompanyData.company_name.ilike(f'%{company_name}%')
        ).limit(5).all()
        suggestions.extend([company.to_dict() for company in companies])
    
    # Rechercher par industrie si pas assez de résultats
    if len(suggestions) < 3 and industry:
        companies = CompanyData.query.filter(
            CompanyData.industry.ilike(f'%{industry}%')
        ).limit(5).all()
        suggestions.extend([company.to_dict() for company in companies])
    
    # Supprimer les doublons
    seen_ids = set()
    unique_suggestions = []
    for suggestion in suggestions:
        if suggestion['id'] not in seen_ids:
            unique_suggestions.append(suggestion)
            seen_ids.add(suggestion['id'])
    
    return jsonify({
        'suggestions': unique_suggestions[:5],
        'count': len(unique_suggestions)
    }), 200

def generate_business_plan_content(template_content, variables, company_name):
    """Générer le contenu du business plan à partir du template et des variables"""
    
    # Remplacer les variables dans le template
    content = template_content
    
    # Variables par défaut
    default_variables = {
        'company_name': company_name,
        'date': datetime.now().strftime('%d/%m/%Y'),
        'year': datetime.now().year
    }
    
    # Fusionner avec les variables fournies
    all_variables = {**default_variables, **variables}
    
    # Remplacer les placeholders dans le template
    for key, value in all_variables.items():
        placeholder = f'{{{{{key}}}}}'  # Format {{variable_name}}
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False, indent=2)
        content = content.replace(placeholder, str(value))
    
    return content

def export_business_plan_to_file(content, company_name, format='pdf'):
    """Exporter le business plan vers un fichier"""
    
    # Créer le dossier d'export s'il n'existe pas
    export_dir = os.path.join(os.path.dirname(__file__), '..', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    # Nom de fichier sécurisé
    safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{safe_company_name}_{timestamp}.{format}"
    file_path = os.path.join(export_dir, filename)
    
    if format == 'pdf':
        # Exporter en PDF (nécessite weasyprint ou reportlab)
        try:
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            # CSS pour le styling
            css_content = """
            @page {
                margin: 2cm;
                @top-center {
                    content: "Business Plan - """ + company_name + """";
                    font-size: 12px;
                    color: #666;
                }
                @bottom-center {
                    content: "Page " counter(page) " sur " counter(pages);
                    font-size: 10px;
                    color: #666;
                }
            }
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 30px; }
            h3 { color: #7f8c8d; }
            .header { text-align: center; margin-bottom: 40px; }
            .section { margin-bottom: 30px; }
            """
            
            # Convertir le contenu markdown en HTML si nécessaire
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Business Plan - {company_name}</title>
            </head>
            <body>
                <div class="header">
                    <h1>Business Plan</h1>
                    <h2>{company_name}</h2>
                    <p>Généré le {datetime.now().strftime('%d/%m/%Y')}</p>
                </div>
                <div class="content">
                    {content.replace(chr(10), '<br>')}
                </div>
            </body>
            </html>
            """
            
            HTML(string=html_content).write_pdf(
                file_path,
                stylesheets=[CSS(string=css_content)]
            )
            
        except ImportError:
            # Fallback: utiliser reportlab
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Titre
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center
            )
            story.append(Paragraph(f"Business Plan - {company_name}", title_style))
            story.append(Spacer(1, 20))
            
            # Contenu
            content_style = styles['Normal']
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), content_style))
                    story.append(Spacer(1, 12))
            
            doc.build(story)
    
    elif format == 'html':
        # Exporter en HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Business Plan - {company_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .header {{ text-align: center; margin-bottom: 40px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Business Plan</h1>
                <h2>{company_name}</h2>
                <p>Généré le {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
            <div class="content">
                {content.replace(chr(10), '<br>')}
            </div>
        </body>
        </html>
        """
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    elif format == 'txt':
        # Exporter en texte brut
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Business Plan - {company_name}\n")
            f.write(f"Généré le {datetime.now().strftime('%d/%m/%Y')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(content)
    
    return file_path

