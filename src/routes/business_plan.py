from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os
import json

from src.models.database import db, BusinessPlan, BusinessPlanTemplate, User, Conversation, CompanyData
from src.services.weather_service import WeatherService
from src.services.enhanced_pdf_generator import EnhancedPDFGenerator
from src.services.unit_converter import UnitConverter
from src.models.payment_models import Subscription
from src.routes.payment import get_package_features
from src.services.pineapple_service import PineappleService

business_plan_bp = Blueprint('business_plan', __name__)

weather_service = WeatherService()
pdf_generator = EnhancedPDFGenerator()
pineapple_service = PineappleService()

def check_user_subscription(user_id: int) -> dict:
    """
    Vérifie l'abonnement de l'utilisateur
    
    Args:
        user_id (int): ID de l'utilisateur
        
    Returns:
        dict: Fonctionnalités disponibles
    """
    try:
        # Récupérer l'abonnement actif
        subscription = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if subscription and subscription.is_active:
            return get_package_features(subscription.package_id)
        else:
            return get_package_features('free')
            
    except Exception as e:
        print(f"Erreur vérification abonnement: {e}")
        return get_package_features('free')

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

@business_plan_bp.route('/generate-enhanced', methods=['POST'])
@jwt_required()
def generate_enhanced_business_plan():
    """
    Génère un business plan enrichi avec météo et plan d'action
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Récupérer l'utilisateur
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Vérifier l'abonnement
        features = check_user_subscription(user_id)
        
        if not features.get('pdf_premium', False):
            return jsonify({
                'error': 'Fonctionnalité premium',
                'message': 'Cette fonctionnalité nécessite un abonnement Premium ou Coopérative',
                'upgrade_required': True
            }), 403
        
        # Récupérer les données météo
        weather_data = None
        if user.zone_agro_ecologique:
            weather_data = weather_service.get_agro_advice(
                user.zone_agro_ecologique, 
                user.primary_culture or 'mais'
            )
        
        # Préparer les données utilisateur
        user_data = {
            'username': user.username or f"{user.first_name} {user.last_name}",
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'zone_agro_ecologique': user.zone_agro_ecologique,
            'farming_objective': user.farming_objective,
            'land_area': user.land_area,
            'land_unit': user.land_unit,
            'farming_experience': user.farming_experience,
            'primary_culture': user.primary_culture,
            'cooperative_name': user.cooperative_name,
            'cooperative_members': user.cooperative_members,
            'cooperative_commune': user.cooperative_commune
        }
        
        # Convertir les unités si nécessaire
        if user.land_area and user.land_unit:
            standard_area = UnitConverter.get_standard_area(user.land_area, user.land_unit)
            user_data['land_area_ha'] = standard_area['ha']
            user_data['land_area_m2'] = standard_area['m2']
        
        # Données business de base
        business_data = {
            'operating_costs': 150000,  # À calculer selon la surface
            'fixed_costs': 50000,
            'expected_revenue': 300000,
            'gross_margin': 150000,
            'net_result': 100000
        }
        
        # Générer le PDF enrichi
        pdf_path = pdf_generator.generate_business_plan_pdf(
            user_data=user_data,
            weather_data=weather_data,
            business_data=business_data
        )
        
        # Créer l'entrée en base
        business_plan = BusinessPlan(
            user_id=user_id,
            company_name=f"Exploitation {user_data['username']}",
            generated_content=json.dumps({
                'user_data': user_data,
                'weather_data': weather_data,
                'business_data': business_data
            }),
            variables_used=json.dumps(data),
            file_path=pdf_path,
            file_format='pdf',
            status='generated'
        )
        
        db.session.add(business_plan)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Business plan enrichi généré avec succès',
            'file_path': pdf_path,
            'business_plan_id': business_plan.id,
            'weather_data': weather_data
        })
        
    except Exception as e:
        print(f"Erreur génération business plan enrichi: {e}")
        return jsonify({'error': 'Erreur lors de la génération'}), 500

@business_plan_bp.route('/pineapple/generate', methods=['POST'])
@jwt_required()
def generate_pineapple_business_plan():
    """
    Génère un business plan ananas
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Récupérer l'utilisateur
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Vérifier l'abonnement
        features = check_user_subscription(user_id)
        
        if not features.get('business_plan_basic', False):
            return jsonify({
                'error': 'Fonctionnalité premium',
                'message': 'Cette fonctionnalité nécessite un abonnement',
                'upgrade_required': True
            }), 403
        
        # Préparer les données utilisateur
        user_data = {
            'zone_agro_ecologique': user.zone_agro_ecologique or 'Zone des terres de barre',
            'land_area': user.land_area or 1.0,
            'farming_experience': user.farming_experience or 'Débutant',
            'farming_objective': user.farming_objective or 'Commercial'
        }
        
        # Récupérer la variété
        variety_id = data.get('variety_id', 1)
        
        # Générer le business plan ananas
        business_plan = pineapple_service.generate_pineapple_business_plan(user_data, variety_id)
        
        if not business_plan:
            return jsonify({'error': 'Erreur lors de la génération du business plan ananas'}), 500
        
        # Générer le PDF si demandé
        pdf_path = None
        if data.get('generate_pdf', False) and features.get('pdf_premium', False):
            try:
                pdf_generator = EnhancedPDFGenerator()
                pdf_path = pdf_generator.generate_pineapple_business_plan_pdf(business_plan)
            except Exception as e:
                print(f"Erreur génération PDF ananas: {e}")
        
        return jsonify({
            'success': True,
            'business_plan': business_plan,
            'pdf_path': pdf_path
        })
        
    except Exception as e:
        print(f"Erreur génération business plan ananas: {e}")
        return jsonify({'error': 'Erreur lors de la génération'}), 500

@business_plan_bp.route('/pineapple/varieties', methods=['GET'])
def get_pineapple_varieties():
    """
    Récupère les variétés d'ananas disponibles
    """
    try:
        zone = request.args.get('zone')
        varieties = pineapple_service.get_varieties(zone)
        
        return jsonify({
            'success': True,
            'varieties': varieties
        })
        
    except Exception as e:
        print(f"Erreur récupération variétés ananas: {e}")
        return jsonify({'error': 'Erreur lors de la récupération'}), 500

@business_plan_bp.route('/pineapple/techniques', methods=['GET'])
def get_pineapple_techniques():
    """
    Récupère les techniques culturales ananas
    """
    try:
        category = request.args.get('category')
        zone = request.args.get('zone')
        
        techniques = pineapple_service.get_techniques(category, zone)
        
        return jsonify({
            'success': True,
            'techniques': techniques
        })
        
    except Exception as e:
        print(f"Erreur récupération techniques ananas: {e}")
        return jsonify({'error': 'Erreur lors de la récupération'}), 500

@business_plan_bp.route('/pineapple/diseases', methods=['GET'])
def get_pineapple_diseases():
    """
    Récupère les maladies de l'ananas
    """
    try:
        severity = request.args.get('severity')
        diseases = pineapple_service.get_diseases(severity)
        
        return jsonify({
            'success': True,
            'diseases': diseases
        })
        
    except Exception as e:
        print(f"Erreur récupération maladies ananas: {e}")
        return jsonify({'error': 'Erreur lors de la récupération'}), 500

@business_plan_bp.route('/pineapple/advice', methods=['GET'])
def get_pineapple_advice():
    """
    Récupère les conseils ananas
    """
    try:
        zone = request.args.get('zone', 'Zone des terres de barre')
        variety = request.args.get('variety')
        season = request.args.get('season')
        
        advice = pineapple_service.get_pineapple_advice(zone, variety, season)
        
        return jsonify({
            'success': True,
            'advice': advice
        })
        
    except Exception as e:
        print(f"Erreur récupération conseils ananas: {e}")
        return jsonify({'error': 'Erreur lors de la récupération'}), 500

@business_plan_bp.route('/pineapple/market-data', methods=['GET'])
def get_pineapple_market_data():
    """
    Récupère les données de marché ananas
    """
    try:
        zone = request.args.get('zone', 'Zone des terres de barre')
        variety = request.args.get('variety')
        month = request.args.get('month')
        
        if month:
            month = int(month)
        
        market_data = pineapple_service.get_market_data(zone, variety, month)
        
        return jsonify({
            'success': True,
            'market_data': market_data
        })
        
    except Exception as e:
        print(f"Erreur récupération données marché ananas: {e}")
        return jsonify({'error': 'Erreur lors de la récupération'}), 500

@business_plan_bp.route('/pineapple/economic-data', methods=['GET'])
def get_pineapple_economic_data():
    """
    Récupère les données économiques ananas
    """
    try:
        zone = request.args.get('zone', 'Zone des terres de barre')
        variety = request.args.get('variety')
        
        economic_data = pineapple_service.get_economic_data(zone, variety)
        
        return jsonify({
            'success': True,
            'economic_data': economic_data
        })
        
    except Exception as e:
        print(f"Erreur récupération données économiques ananas: {e}")
        return jsonify({'error': 'Erreur lors de la récupération'}), 500

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

@business_plan_bp.route('/weather/<zone>', methods=['GET'])
def get_weather_data(zone):
    """
    Récupère les données météo pour une zone
    """
    try:
        weather_data = weather_service.get_current_weather(zone)
        forecast_data = weather_service.get_forecast(zone, 7)
        agro_advice = weather_service.get_agro_advice(zone, 'mais')
        
        return jsonify({
            'current_weather': weather_data,
            'forecast': forecast_data,
            'agro_advice': agro_advice
        })
        
    except Exception as e:
        print(f"Erreur récupération météo: {e}")
        return jsonify({'error': 'Erreur lors de la récupération météo'}), 500

@business_plan_bp.route('/action-plan/<user_id>', methods=['GET'])
def get_action_plan(user_id):
    """
    Génère un plan d'action personnalisé
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Récupérer les données météo
        weather_data = None
        if user.zone_agro_ecologique:
            weather_data = weather_service.get_agro_advice(
                user.zone_agro_ecologique, 
                user.primary_culture or 'mais'
            )
        
        # Générer le plan d'action
        current_month = datetime.now().month
        culture = user.primary_culture or 'mais'
        
        if culture.lower() == 'mais':
            plan_30 = pdf_generator._get_mais_30_days_plan(current_month, weather_data)
            plan_60 = pdf_generator._get_mais_60_days_plan(current_month, weather_data)
            plan_90 = pdf_generator._get_mais_90_days_plan(current_month, weather_data)
        else:
            plan_30 = ["Préparation", "Planification", "Organisation"]
            plan_60 = ["Exécution", "Suivi", "Ajustements"]
            plan_90 = ["Évaluation", "Amélioration", "Préparation suivante"]
        
        action_plan = {
            'user_info': {
                'name': f"{user.first_name} {user.last_name}",
                'zone': user.zone_agro_ecologique,
                'culture': culture,
                'surface': f"{user.land_area} {user.land_unit}" if user.land_area else "Non spécifiée"
            },
            'weather_data': weather_data,
            'action_plan': {
                '30_days': plan_30,
                '60_days': plan_60,
                '90_days': plan_90
            }
        }
        
        return jsonify(action_plan)
        
    except Exception as e:
        print(f"Erreur génération plan d'action: {e}")
        return jsonify({'error': 'Erreur lors de la generation du plan d\'action'}), 500

@business_plan_bp.route('/features', methods=['GET'])
@jwt_required()
def get_available_features():
    """
    Récupère les fonctionnalités disponibles pour l'utilisateur
    """
    try:
        user_id = get_jwt_identity()
        features = check_user_subscription(user_id)
        
        return jsonify({
            'success': True,
            'features': features
        })
        
    except Exception as e:
        print(f"Erreur récupération fonctionnalités: {e}")
        return jsonify({'error': 'Erreur lors de la récupération'}), 500

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

