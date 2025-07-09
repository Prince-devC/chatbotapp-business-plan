import os
import google.generativeai as genai
from typing import List, Dict, Any
import json
import logging
from pathlib import Path
import PyPDF2
from docx import Document
import pandas as pd
from io import BytesIO

logger = logging.getLogger(__name__)

class GeminiAnalysisService:
    def __init__(self):
        # Configuration de Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        
        # Détecter les clés API factices ou invalides
        invalid_keys = [
            'AIzaSyClXQC_Xx1FyI4wU-jZjY7ZCIpGahR9n_M',  # Clé exemple du fichier .env
            'your-api-key-here',
            'fake-key',
            'test-key'
        ]
        
        if not api_key or api_key.strip() == '' or api_key in invalid_keys:
            logger.warning("🎭 GEMINI_API_KEY manquante ou invalide - Mode DEMO activé")
            self.model = None
            self.demo_mode = True
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')
                self.demo_mode = False
                logger.info("✅ Service Gemini initialisé avec succès")
            except Exception as e:
                logger.error(f"❌ Erreur initialisation Gemini: {str(e)} - Mode DEMO activé")
                self.model = None
                self.demo_mode = True
        
    def _resolve_file_path(self, file_path: str) -> str:
        """Résout le chemin de fichier en tenant compte de l'environnement d'exécution."""
        try:
            # Si le chemin est déjà absolu et existe, le retourner tel quel
            if os.path.isabs(file_path) and os.path.exists(file_path):
                return file_path
            
            # Essayer de résoudre depuis la racine du projet
            project_root = Path(__file__).parent.parent.parent.resolve()
            
            # Si c'est un chemin relatif (commence par uploads/), le résoudre depuis la racine du projet
            if file_path.startswith('uploads/'):
                resolved_path = project_root / file_path
                if resolved_path.exists():
                    return str(resolved_path)
            
            # Si c'est un chemin relatif, essayer de le résoudre depuis le répertoire de travail actuel
            if not os.path.isabs(file_path):
                # Essayer depuis le répertoire de travail actuel
                resolved_path = os.path.abspath(file_path)
                if os.path.exists(resolved_path):
                    return resolved_path
                
                # Essayer depuis la racine du projet
                resolved_path = project_root / file_path
                if resolved_path.exists():
                    return str(resolved_path)
            
            # Si le chemin contient déjà le nom du projet, essayer de le reconstruire
            if 'chatbotapp-business-plan' in file_path:
                # Extraire le chemin relatif après 'chatbotapp-business-plan'
                parts = file_path.split('chatbotapp-business-plan')
                if len(parts) > 1:
                    relative_path = parts[1].lstrip('/')
                    resolved_path = project_root / relative_path
                    if resolved_path.exists():
                        return str(resolved_path)
            
            # Essayer de construire le chemin depuis la racine du projet
            # En supposant que le fichier est dans uploads/templates/
            filename = os.path.basename(file_path)
            uploads_path = project_root / 'uploads' / 'templates' / filename
            if uploads_path.exists():
                return str(uploads_path)
            
            # Si rien ne fonctionne, retourner le chemin original
            logger.warning(f"Impossible de résoudre le chemin: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Erreur lors de la résolution du chemin {file_path}: {str(e)}")
            return file_path
        
    def extract_text_from_file(self, file_path: str, file_type: str) -> str:
        """Extrait le texte d'un fichier selon son type."""
        try:
            # Résoudre le chemin du fichier
            resolved_path = self._resolve_file_path(file_path)
            logger.info(f"Tentative d'extraction depuis: {resolved_path}")
            
            if not os.path.exists(resolved_path):
                logger.error(f"Fichier non trouvé: {resolved_path}")
                return ""
            
            if file_type.lower() == 'pdf':
                return self._extract_from_pdf(resolved_path)
            elif file_type.lower() in ['doc', 'docx']:
                return self._extract_from_docx(resolved_path)
            elif file_type.lower() == 'txt':
                return self._extract_from_txt(resolved_path)
            elif file_type.lower() in ['xls', 'xlsx']:
                return self._extract_from_excel(resolved_path)
            else:
                logger.warning(f"Type de fichier non supporté: {file_type}")
                return ""
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction de {file_path}: {str(e)}")
            return ""
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extrait le texte d'un fichier PDF."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extrait le texte d'un fichier Word."""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Erreur extraction DOCX: {str(e)}")
            return ""
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extrait le texte d'un fichier texte."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Erreur extraction TXT: {str(e)}")
            return ""
    
    def _extract_from_excel(self, file_path: str) -> str:
        """Extrait les données d'un fichier Excel."""
        try:
            df = pd.read_excel(file_path, sheet_name=None)
            text = ""
            for sheet_name, sheet_data in df.items():
                text += f"\n=== Feuille: {sheet_name} ===\n"
                text += sheet_data.to_string(index=False) + "\n"
            return text
        except Exception as e:
            logger.error(f"Erreur extraction Excel: {str(e)}")
            return ""
    
    def _is_greeting(self, user_request: str) -> bool:
        """Vérifie si la requête est une salutation."""
        greeting_keywords = [
            'bonjour', 'salut', 'hello', 'hi', 'coucou', 'bonsoir',
            'bonne journée', 'bonne soirée', 'comment allez-vous',
            'ça va', 'comment ça va', 'comment allez vous'
        ]
        
        request_lower = user_request.lower()
        return any(keyword in request_lower for keyword in greeting_keywords)
    
    def _is_mais_related(self, user_request: str) -> bool:
        """Vérifie si la requête est liée spécifiquement au maïs."""
        mais_keywords = [
            'mais', 'maïs', 'corn', 'zea mays',
            'culture de maïs', 'plantation de maïs', 'production de maïs',
            'maïs grain', 'maïs fourrage', 'maïs doux',
            'semis de maïs', 'récolte de maïs', 'irrigation maïs',
            'fertilisation maïs', 'traitement maïs'
        ]
        
        request_lower = user_request.lower()
        return any(keyword in request_lower for keyword in mais_keywords)
    
    def _is_unlock_attempt(self, user_request: str) -> bool:
        """Vérifie si la requête est une tentative de déblocage avec le code d'accès."""
        return user_request.strip() == "join-mais-ai-generate"

    def analyze_documents_for_business_plan(self, templates: List[Dict], user_request: str, user_id: str = None) -> Dict[str, Any]:
        """Analyse tous les templates de la base pour créer un business plan suivant strictement leur structure."""
        
        # Vérifier si c'est une salutation
        if self._is_greeting(user_request):
            return {
                'success': True,
                'is_greeting': True,
                'greeting_response': f"Bonjour ! Je suis votre assistant IA spécialisé dans la culture de maïs. Je peux vous aider à créer un business plan complet pour votre projet de culture de maïs. Dites-moi ce que vous souhaitez faire !",
                'documents_analyzed': 0,
                'demo_mode': self.demo_mode
            }
        
        # Vérifier si c'est une tentative de déblocage
        if self._is_unlock_attempt(user_request):
            from src.services.rate_limiter import rate_limiter
            if user_id:
                success, message = rate_limiter.unlock_user(user_id, user_request.strip())
                return {
                    'success': True,
                    'is_unlock_attempt': True,
                    'unlock_success': success,
                    'unlock_message': message,
                    'documents_analyzed': 0,
                    'demo_mode': self.demo_mode
                }
            else:
                return {
                    'success': False,
                    'error': "Impossible de traiter le code de déblocage sans identifiant utilisateur",
                    'documents_analyzed': 0,
                    'demo_mode': self.demo_mode
                }
        
        # Vérifier le rate limiting
        if user_id:
            from src.services.rate_limiter import rate_limiter
            can_request, message = rate_limiter.can_make_request(user_id)
            if not can_request:
                return {
                    'success': False,
                    'error': message,
                    'is_rate_limited': True,
                    'documents_analyzed': 0,
                    'demo_mode': self.demo_mode
                }
        
        # Vérifier si la requête est liée au maïs
        if not self._is_mais_related(user_request):
            return {
                'success': False,
                'error': "Désolé, je suis spécialisé uniquement dans la culture de maïs. Veuillez reformuler votre demande en lien avec le maïs (ex: culture de maïs sur 10 ha, production de maïs grain, etc.)",
                'documents_analyzed': 0,
                'demo_mode': self.demo_mode
            }

        # Extraire et analyser le contenu de tous les templates
        documents_content = []
        business_plan_templates = []
        itinerary_templates = []
        
        for template in templates:
            if template.get('file_path'):
                content = self.extract_text_from_file(
                    template['file_path'], 
                    template.get('file_type', '')
                )
                if content.strip():
                    template_data = {
                        'name': template.get('name', 'Document sans nom'),
                        'category': template.get('category', 'Général'),
                        'content': content,
                        'type': template.get('file_type', 'unknown'),
                        'file_path': template.get('file_path', '')
                    }
                    
                    documents_content.append(template_data)
                    
                    # Classifier les templates selon leur contenu
                    content_lower = content.lower()
                    if any(keyword in content_lower for keyword in ['business plan', 'plan d\'affaires', 'business', 'marché', 'financier', 'revenus']):
                        business_plan_templates.append(template_data)
                    elif any(keyword in content_lower for keyword in ['itinéraire', 'technique', 'développement', 'implémentation', 'architecture']):
                        itinerary_templates.append(template_data)
                    else:
                        # Ajouter aux deux catégories si non spécifique
                        business_plan_templates.append(template_data)
                        itinerary_templates.append(template_data)
        
        logger.info(f"📋 Templates analysés: {len(business_plan_templates)} business plan, {len(itinerary_templates)} techniques")
        
        try:
            if self.demo_mode:
                # Mode démo - analyser les templates réels et adapter le contenu
                logger.info("🎭 Mode DEMO - Analyse des templates réels de la base de données")
                business_plan_data = self._generate_plan_from_templates(
                    user_request, 
                    business_plan_templates, 
                    itinerary_templates
                )
            else:
                # Mode normal avec Gemini
                logger.info("🤖 Mode GEMINI - Analyse avec IA des templates")
                prompt = self._create_analysis_prompt(documents_content, user_request)
                response = self.model.generate_content(prompt)
                business_plan_data = json.loads(response.text)
            
            logger.info(f"✅ Business plan généré avec succès (mode: {'DEMO' if self.demo_mode else 'GEMINI'})")
            
            # Incrémenter le compteur de requêtes si un user_id est fourni
            if user_id:
                from src.services.rate_limiter import rate_limiter
                rate_limiter.increment_request(user_id)
                logger.info(f"📊 Compteur incrémenté pour l'utilisateur {user_id}")
            
            return {
                'success': True,
                'business_plan': business_plan_data,
                'documents_analyzed': len(documents_content),
                'business_plan_templates': len(business_plan_templates),
                'itinerary_templates': len(itinerary_templates),
                'user_request': user_request,
                'demo_mode': self.demo_mode
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'documents_analyzed': len(documents_content),
                'demo_mode': getattr(self, 'demo_mode', True)
            }
    
    def _generate_plan_from_templates(self, user_request: str, business_plan_templates: List[Dict], itinerary_templates: List[Dict]) -> Dict[str, Any]:
        """Génère un business plan en analysant le contenu réel des templates de la base de données."""
        
        # Analyser le contenu des templates business plan
        bp_content_analysis = self._analyze_template_content(business_plan_templates)
        itinerary_content_analysis = self._analyze_template_content(itinerary_templates)
        
        # Adapter le contenu au projet utilisateur
        adapted_content = self._adapt_content_to_request(user_request, bp_content_analysis, itinerary_content_analysis)
        
        return adapted_content
    
    def _analyze_template_content(self, templates: List[Dict]) -> Dict[str, Any]:
        """Analyse le contenu des templates pour extraire la structure et les informations clés."""
        analysis = {
            'structure_detected': [],
            'key_sections': [],
            'financial_data': [],
            'market_insights': [],
            'technical_elements': [],
            'content_samples': []
        }
        
        for template in templates:
            content = template['content']
            lines = content.split('\n')
            
            # Détecter les sections principales
            for line in lines:
                line_clean = line.strip()
                if line_clean:
                    # Détecter les titres (lignes courtes en majuscules ou avec des mots-clés)
                    if len(line_clean) < 100 and any(keyword in line_clean.lower() for keyword in [
                        'résumé', 'exécutif', 'marché', 'analyse', 'stratégie', 'marketing', 
                        'financier', 'opérationnel', 'risque', 'équipe', 'itinéraire', 
                        'technique', 'développement', 'architecture', 'implémentation'
                    ]):
                        analysis['structure_detected'].append(line_clean)
                    
                    # Extraire des échantillons de contenu
                    if 20 < len(line_clean) < 200:
                        analysis['content_samples'].append(line_clean)
            
            # Détecter les éléments financiers
            financial_keywords = ['budget', 'coût', 'prix', 'chiffre', 'affaires', 'revenus', 'bénéfice', 'investissement']
            for line in lines:
                if any(keyword in line.lower() for keyword in financial_keywords):
                    analysis['financial_data'].append(line.strip())
            
            # Détecter les éléments techniques
            technical_keywords = ['technologie', 'développement', 'architecture', 'système', 'plateforme', 'API', 'base de données']
            for line in lines:
                if any(keyword in line.lower() for keyword in technical_keywords):
                    analysis['technical_elements'].append(line.strip())
        
        return analysis
    
    def _adapt_content_to_request(self, user_request: str, bp_analysis: Dict, itinerary_analysis: Dict) -> Dict[str, Any]:
        """Adapte le contenu des templates à la demande spécifique de l'utilisateur."""
        
        # Extraire le type de projet de la demande utilisateur
        project_type = self._extract_project_type(user_request)
        
        # Utiliser la structure détectée dans les templates
        structure_elements = list(set(bp_analysis['structure_detected'] + itinerary_analysis['structure_detected']))
        content_samples = bp_analysis['content_samples'][:10]  # Limiter les échantillons
        
        return {
            "titre": f"Business Plan - {project_type}",
            "resume_executif": {
                "description_projet": f"Projet de {project_type} basé sur la demande: {user_request}. Structure suivant les templates analysés: {', '.join(structure_elements[:3])}.",
                "marche_cible": f"Marché ciblé pour {project_type} selon l'analyse des templates de référence",
                "avantage_concurrentiel": f"Positionnement concurrentiel adapté au secteur {project_type}",
                "projections_financieres": "Projections basées sur les modèles financiers des templates analysés" if bp_analysis['financial_data'] else "Projections à établir selon le modèle détecté",
                "financement_requis": "Besoins déterminés selon les structures template analysées"
            },
            "analyse_marche": {
                "taille_marche": f"Marché du secteur {project_type} selon l'analyse des données templates",
                "segmentation": "Segments identifiés dans les templates de référence",
                "tendances": f"Tendances extraites des {len(bp_analysis['content_samples'])} échantillons d'analyse",
                "concurrence": "Analyse concurrentielle basée sur les méthodologies des templates",
                "opportunites": f"Opportunités spécifiques au {project_type} selon les templates"
            },
            "strategie_marketing": {
                "positionnement": f"Positionnement {project_type} selon les approches détectées",
                "mix_marketing": "Stratégie adaptée aux modèles des templates analysés",
                "canaux_distribution": f"Canaux optimaux pour {project_type} selon les références",
                "plan_communication": "Plan basé sur les structures template détectées",
                "budget_marketing": "Budget selon les ratios identifiés dans les templates"
            },
            "plan_operationnel": {
                "processus_production": f"Processus {project_type} selon les méthodologies templates",
                "ressources_necessaires": "Ressources selon l'analyse des templates de référence",
                "partenaires": f"Partenaires stratégiques identifiés pour {project_type}",
                "localisation": "Localisation selon les critères des templates analysés",
                "technologie": "Stack technologique extraite des templates techniques"
            },
            "projections_financieres": self._generate_financial_projections_from_templates(project_type, bp_analysis),
            "equipe": {
                "dirigeants": f"Profils dirigeants pour {project_type} selon les templates",
                "competences_cles": "Compétences extraites de l'analyse des templates",
                "recrutements_prevus": "Plan de recrutement selon les modèles analysés",
                "conseil": "Structure de conseil selon les templates de référence"
            },
            "risques_opportunites": {
                "risques_identifies": f"Risques spécifiques au {project_type} selon l'analyse",
                "mesures_mitigation": "Mesures selon les approches des templates",
                "opportunites_croissance": f"Opportunités {project_type} identifiées",
                "scenarios": "Scénarios selon les méthodologies des templates"
            },
            "itineraire_technique": self._generate_technical_itinerary_from_templates(project_type, itinerary_analysis),
            "annexes": {
                "templates_analyses": f"{len(structure_elements)} sections template détectées",
                "echantillons_contenu": content_samples[:3],
                "sources_donnees": f"Basé sur l'analyse de {len(bp_analysis['content_samples']) + len(itinerary_analysis['content_samples'])} éléments template",
                "structure_reference": structure_elements[:5]
            },
            "recommandations": {
                "prochaines_etapes": f"Étapes pour {project_type} selon les templates analysés",
                "conseils_implementation": "Conseils extraits des méthodologies template",
                "indicateurs_suivi": f"KPIs {project_type} selon les références analysées",
                "mise_a_jour": "Mise à jour selon les cycles identifiés dans les templates"
            }
        }
    
    def _extract_project_type(self, user_request: str) -> str:
        """Extrait le type de projet agricole de la demande utilisateur."""
        request_lower = user_request.lower()
        
        # Cultures
        if any(word in request_lower for word in ['mais', 'maïs']):
            return 'culture de maïs'
        elif 'manioc' in request_lower:
            return 'culture de manioc'
        elif 'riz' in request_lower:
            return 'culture de riz'
        elif 'soja' in request_lower:
            return 'culture de soja'
        elif any(word in request_lower for word in ['maraîcher', 'légume', 'fruit']):
            return 'maraîchage'
        
        # Élevage
        elif any(word in request_lower for word in ['volaille', 'poulet', 'poule']):
            return 'élevage de volailles'
        elif any(word in request_lower for word in ['bovin', 'vache', 'boeuf']):
            return 'élevage bovin'
        elif any(word in request_lower for word in ['porc', 'porcin']):
            return 'élevage porcin'
        elif any(word in request_lower for word in ['mouton', 'ovin', 'chèvre', 'caprin']):
            return 'élevage ovin/caprin'
        elif 'élevage' in request_lower:
            return 'projet d\'élevage'
            
        # Agriculture spécialisée
        elif 'bio' in request_lower or 'biologique' in request_lower:
            return 'agriculture biologique'
        elif 'permaculture' in request_lower:
            return 'projet de permaculture'
        elif 'serre' in request_lower or 'greenhouse' in request_lower:
            return 'culture sous serre'
        
        # Par défaut
        else:
            return 'projet agricole'
    
    def _generate_financial_projections_from_templates(self, project_type: str, bp_analysis: Dict) -> Dict[str, Any]:
        """Génère des projections financières basées sur les templates analysés."""
        
        # Adapter selon le type de projet et les données template
        base_revenue = 100000 if 'service' in project_type else 150000
        
        return {
            "compte_resultat_3ans": {
                "annee_1": {"chiffre_affaires": base_revenue, "charges": int(base_revenue * 0.8), "resultat": int(base_revenue * 0.2)},
                "annee_2": {"chiffre_affaires": int(base_revenue * 1.8), "charges": int(base_revenue * 1.3), "resultat": int(base_revenue * 0.5)},
                "annee_3": {"chiffre_affaires": int(base_revenue * 3), "charges": int(base_revenue * 2), "resultat": base_revenue}
            },
            "plan_financement": {
                "investissement_initial": int(base_revenue * 0.5),
                "besoin_fonds_roulement": int(base_revenue * 0.2),
                "sources_financement": f"Financement adapté au {project_type} selon templates"
            },
            "seuil_rentabilite": f"Seuil atteint selon les modèles {project_type} des templates",
            "hypotheses": f"Hypothèses basées sur {len(bp_analysis['financial_data'])} éléments financiers des templates"
        }
    
    def _generate_technical_itinerary_from_templates(self, project_type: str, itinerary_analysis: Dict) -> Dict[str, Any]:
        """Génère l'itinéraire technique basé sur les templates analysés."""
        
        technical_elements = itinerary_analysis.get('technical_elements', [])
        
        return {
            "etapes_developpement": f"Développement {project_type} selon les phases identifiées dans les templates techniques analysés",
            "planning_implementation": f"Planning basé sur les méthodologies des {len(technical_elements)} éléments techniques extraits",
            "ressources_techniques": f"Équipe technique adaptée au {project_type} selon les templates",
            "specifications": f"Spécifications {project_type} suivant les structures template détectées",
            "architecture": f"Architecture adaptée au {project_type} selon les modèles analysés",
            "technologies": f"Technologies extraites de l'analyse des templates techniques",
            "contraintes": f"Contraintes {project_type} identifiées dans les templates de référence",
            "solutions_alternatives": f"Solutions selon les approches des templates analysés"
        }

    def _generate_demo_business_plan(self, user_request: str, documents_count: int) -> Dict[str, Any]:
        """Génère un business plan basé strictement sur l'analyse des templates de la base de données."""
        return {
            "titre": f"Business Plan - {user_request[:50]}...",
            "resume_executif": {
                "description_projet": f"Projet d'entreprise basé sur: {user_request}. Ce plan suit rigoureusement la structure et le contenu des {documents_count} templates analysés de notre base de données.",
                "marche_cible": "Segment de marché identifié selon l'analyse des templates sectoriels de la base",
                "avantage_concurrentiel": "Positionnement concurrentiel déterminé par l'analyse comparative des documents de référence",
                "projections_financieres": "Projections établies selon les modèles financiers des templates analysés",
                "financement_requis": "Besoins de financement calculés selon les structures des templates de la base"
            },
            "analyse_marche": {
                "taille_marche": "Marché évalué selon les données disponibles",
                "segmentation": "Segments identifiés par l'analyse IA",
                "tendances": "Tendances extraites des documents analysés",
                "concurrence": "Analyse concurrentielle basée sur les templates",
                "opportunites": "Opportunités détectées automatiquement"
            },
            "strategie_marketing": {
                "positionnement": "Positionnement stratégique recommandé",
                "mix_marketing": "Stratégie 4P adaptée au projet",
                "canaux_distribution": "Canaux optimaux selon l'analyse",
                "plan_communication": "Plan de communication personnalisé",
                "budget_marketing": "Budget estimé selon les standards"
            },
            "plan_operationnel": {
                "processus_production": "Processus optimisés selon les meilleures pratiques",
                "ressources_necessaires": "Ressources identifiées par l'analyse",
                "partenaires": "Partenaires stratégiques recommandés",
                "localisation": "Localisation optimale selon l'étude",
                "technologie": "Stack technologique recommandée"
            },
            "projections_financieres": {
                "compte_resultat_3ans": {
                    "annee_1": {"chiffre_affaires": 150000, "charges": 120000, "resultat": 30000},
                    "annee_2": {"chiffre_affaires": 250000, "charges": 180000, "resultat": 70000},
                    "annee_3": {"chiffre_affaires": 400000, "charges": 280000, "resultat": 120000}
                },
                "plan_financement": {
                    "investissement_initial": 75000,
                    "besoin_fonds_roulement": 25000,
                    "sources_financement": "Financement initial + levée de fonds"
                },
                "seuil_rentabilite": "Seuil atteint en 18 mois selon les projections",
                "hypotheses": "Hypothèses basées sur l'analyse des documents sectoriels"
            },
            "equipe": {
                "dirigeants": "Profils dirigeants recommandés selon l'analyse",
                "competences_cles": "Compétences identifiées comme critiques",
                "recrutements_prevus": "Plan de recrutement sur 3 ans",
                "conseil": "Conseil d'administration suggéré"
            },
            "risques_opportunites": {
                "risques_identifies": "Risques détectés par l'analyse comparative",
                "mesures_mitigation": "Mesures préventives recommandées",
                "opportunites_croissance": "Opportunités de croissance identifiées",
                "scenarios": "Scénarios optimiste et pessimiste"
            },
            "itineraire_technique": {
                "etapes_developpement": "Phase 1: Conception et prototypage (3 mois)\nPhase 2: Développement MVP (6 mois)\nPhase 3: Tests et optimisation (3 mois)\nPhase 4: Lancement commercial (2 mois)",
                "planning_implementation": "Planning détaillé sur 14 mois avec jalons mensuels",
                "ressources_techniques": "Équipe de 5 développeurs + 2 designers + 1 chef de projet",
                "specifications": "Spécifications techniques adaptées au projet avec architecture modulaire",
                "architecture": "Architecture cloud-native avec microservices pour la scalabilité",
                "technologies": "React/Node.js + PostgreSQL + AWS + Docker + CI/CD",
                "contraintes": "Contraintes de sécurité RGPD + performance + budget",
                "solutions_alternatives": "Solutions de fallback et plans de contingence identifiés"
            },
            "annexes": {
                "etudes_marche": f"Références basées sur {documents_count} documents analysés",
                "documents_juridiques": "Documents juridiques nécessaires identifiés",
                "brevets_licences": "Propriété intellectuelle à protéger",
                "sources_donnees": "Sources de données extraites automatiquement"
            },
            "recommandations": {
                "prochaines_etapes": "1. Validation du concept\n2. Recherche de financement\n3. Constitution de l'équipe",
                "conseils_implementation": "Conseils personnalisés selon l'analyse IA",
                "indicateurs_suivi": "KPIs recommandés pour le pilotage",
                "mise_a_jour": "Mise à jour trimestrielle recommandée"
            }
        }
    
    def _create_analysis_prompt(self, documents: List[Dict], user_request: str) -> str:
        """Crée le prompt optimisé pour l'analyse Gemini."""
        
        documents_summary = ""
        for i, doc in enumerate(documents, 1):
            documents_summary += f"""
Document {i}: {doc['name']} (Catégorie: {doc['category']})
Type: {doc['type']}
Contenu (extrait):
{doc['content'][:2000]}...
---
"""
        
        prompt = f"""
Tu es un expert en business plan et consultant en stratégie d'entreprise. 

DEMANDE DE L'UTILISATEUR: "{user_request}"

DOCUMENTS DISPONIBLES DANS LA BASE DE DONNÉES:
{documents_summary}

MISSION:
Analyse tous ces documents et crée un business plan complet et détaillé basé sur la demande de l'utilisateur. Utilise les informations pertinentes des documents pour enrichir ta réponse.

IMPORTANT - FORMAT DE SORTIE:
- Le BUSINESS PLAN sera généré au format EXCEL (.xlsx) avec plusieurs feuilles détaillées
- L'ITINÉRAIRE TECHNIQUE sera généré au format PDF (.pdf) avec mise en page professionnelle
- Assure-toi que le contenu soit adapté pour ces deux formats de sortie

STRUCTURE REQUISE (RÉPONSE EN JSON):
{{
  "titre": "Titre du Business Plan",
  "resume_executif": {{
    "description_projet": "Description détaillée du projet",
    "marche_cible": "Marché ciblé avec données chiffrées",
    "avantage_concurrentiel": "Avantages concurrentiels identifiés",
    "projections_financieres": "Résumé des projections financières",
    "financement_requis": "Montant et type de financement nécessaire"
  }},
  "analyse_marche": {{
    "taille_marche": "Taille du marché avec sources",
    "segmentation": "Segments de marché identifiés",
    "tendances": "Tendances du marché",
    "concurrence": "Analyse concurrentielle détaillée",
    "opportunites": "Opportunités identifiées"
  }},
  "strategie_marketing": {{
    "positionnement": "Positionnement stratégique",
    "mix_marketing": "Stratégie 4P détaillée",
    "canaux_distribution": "Canaux de distribution",
    "plan_communication": "Plan de communication",
    "budget_marketing": "Budget marketing estimé"
  }},
  "plan_operationnel": {{
    "processus_production": "Processus de production/service",
    "ressources_necessaires": "Ressources humaines et matérielles",
    "partenaires": "Partenaires stratégiques",
    "localisation": "Stratégie de localisation",
    "technologie": "Technologies utilisées"
  }},
  "projections_financieres": {{
    "compte_resultat_3ans": {{
      "annee_1": {{"chiffre_affaires": 0, "charges": 0, "resultat": 0}},
      "annee_2": {{"chiffre_affaires": 0, "charges": 0, "resultat": 0}},
      "annee_3": {{"chiffre_affaires": 0, "charges": 0, "resultat": 0}}
    }},
    "plan_financement": {{
      "investissement_initial": 0,
      "besoin_fonds_roulement": 0,
      "sources_financement": "Détail des sources"
    }},
    "seuil_rentabilite": "Calcul du seuil de rentabilité",
    "hypotheses": "Hypothèses de calcul détaillées"
  }},
  "equipe": {{
    "dirigeants": "Profils des dirigeants",
    "competences_cles": "Compétences clés de l'équipe",
    "recrutements_prevus": "Plan de recrutement",
    "conseil": "Conseil d'administration/consultatif"
  }},
  "risques_opportunites": {{
    "risques_identifies": "Liste des risques avec impact",
    "mesures_mitigation": "Mesures de mitigation",
    "opportunites_croissance": "Opportunités de croissance",
    "scenarios": "Scénarios optimiste/pessimiste"
  }},
  "itineraire_technique": {{
    "etapes_developpement": "Étapes détaillées du développement technique",
    "planning_implementation": "Planning détaillé avec jalons",
    "ressources_techniques": "Ressources techniques nécessaires",
    "specifications": "Spécifications techniques détaillées",
    "architecture": "Architecture technique du projet",
    "technologies": "Stack technologique recommandée",
    "contraintes": "Contraintes techniques identifiées",
    "solutions_alternatives": "Solutions alternatives envisagées"
  }},
  "annexes": {{
    "etudes_marche": "Références aux études de marché",
    "documents_juridiques": "Documents juridiques nécessaires",
    "brevets_licences": "Propriété intellectuelle",
    "sources_donnees": "Sources des données utilisées"
  }},
  "recommandations": {{
    "prochaines_etapes": "Étapes immédiates à suivre",
    "conseils_implementation": "Conseils pour la mise en œuvre",
    "indicateurs_suivi": "KPIs à suivre",
    "mise_a_jour": "Fréquence de mise à jour recommandée"
  }}
}}

INSTRUCTIONS IMPORTANTES:
1. Utilise UNIQUEMENT les informations des documents fournis pour enrichir ton analyse
2. Si certaines données manquent, indique-le clairement avec des estimations réalistes
3. Assure-toi que les projections financières sont cohérentes et réalistes
4. Adapte le business plan au secteur d'activité demandé par l'utilisateur
5. Utilise des données chiffrées quand elles sont disponibles dans les documents
6. L'ITINÉRAIRE TECHNIQUE doit être particulièrement détaillé pour le format PDF
7. Le BUSINESS PLAN doit contenir des tableaux et données pour le format Excel
8. RÉPONSE OBLIGATOIREMENT EN JSON VALIDE

Génère maintenant le business plan complet avec itinéraire technique en JSON:
"""
        
        return prompt
