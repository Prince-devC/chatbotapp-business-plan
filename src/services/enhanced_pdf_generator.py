"""
Service de génération PDF enrichi pour AgroBizChat
Intégration météo, plan d'action et design moderne
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
import base64
from PIL import Image
import io

class EnhancedPDFGenerator:
    """Générateur de PDF enrichi avec météo et plan d'action"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configure les styles personnalisés"""
        # Style titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        ))
        
        # Style sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.darkblue
        ))
        
        # Style météo
        self.styles.add(ParagraphStyle(
            name='WeatherStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.darkblue,
            leftIndent=20
        ))
        
        # Style conseils
        self.styles.add(ParagraphStyle(
            name='AdviceStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            textColor=colors.darkgreen
        ))
    
    def generate_business_plan_pdf(self, user_data: Dict, weather_data: Dict = None, 
                                  business_data: Dict = None, output_path: str = None) -> str:
        """
        Génère un business plan PDF enrichi
        
        Args:
            user_data (dict): Données utilisateur
            weather_data (dict): Données météo
            business_data (dict): Données business
            output_path (str): Chemin de sortie
            
        Returns:
            str: Chemin du fichier généré
        """
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"generated_business_plans/business_plan_{user_data.get('username', 'user')}_{timestamp}.pdf"
        
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Créer le document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Page de garde
        story.extend(self._create_cover_page(user_data))
        story.append(PageBreak())
        
        # Sommaire
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())
        
        # Informations utilisateur
        story.extend(self._create_user_info_section(user_data))
        story.append(PageBreak())
        
        # Section météo et conseils
        if weather_data:
            story.extend(self._create_weather_section(weather_data))
            story.append(PageBreak())
        
        # Plan d'action temporel
        story.extend(self._create_action_plan_section(user_data, weather_data))
        story.append(PageBreak())
        
        # Analyse économique
        if business_data:
            story.extend(self._create_economic_analysis_section(business_data))
            story.append(PageBreak())
        
        # Conseils techniques
        story.extend(self._create_technical_advice_section(user_data))
        
        # Générer le PDF
        doc.build(story)
        
        return output_path
    
    def generate_diagnosis_pdf(self, diagnosis_data: Dict, output_path: str = None) -> str:
        """
        Génère un PDF de diagnostic complet avec photo
        
        Args:
            diagnosis_data (dict): Données du diagnostic
            output_path (str): Chemin de sortie
            
        Returns:
            str: Chemin du fichier généré
        """
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"generated_business_plans/diagnosis_{timestamp}.pdf"
        
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Créer le document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Page de garde diagnostic
        story.extend(self._create_diagnosis_cover_page(diagnosis_data))
        story.append(PageBreak())
        
        # Résumé du diagnostic
        story.extend(self._create_diagnosis_summary(diagnosis_data))
        story.append(PageBreak())
        
        # Photo et analyse
        if diagnosis_data.get('photo_data'):
            story.extend(self._create_photo_analysis_section(diagnosis_data))
            story.append(PageBreak())
        
        # Traitements recommandés
        story.extend(self._create_treatments_section(diagnosis_data))
        story.append(PageBreak())
        
        # Mesures de prévention
        story.extend(self._create_prevention_section(diagnosis_data))
        
        # Générer le PDF
        doc.build(story)
        
        return output_path
    
    def _create_cover_page(self, user_data: Dict) -> List:
        """Crée la page de garde"""
        elements = []
        
        # Titre principal
        title = f"Business Plan Agricole - {user_data.get('primary_culture', 'Maïs').title()}"
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 30))
        
        # Informations de base
        user_info = [
            f"<b>Agriculteur:</b> {user_data.get('first_name', '')} {user_data.get('last_name', '')}",
            f"<b>Zone:</b> {user_data.get('zone_agro_ecologique', 'Non spécifiée')}",
            f"<b>Surface:</b> {user_data.get('land_area', 0)} {user_data.get('land_unit', 'ha')}",
            f"<b>Type:</b> {user_data.get('user_type', 'individuel').title()}",
            f"<b>Culture principale:</b> {user_data.get('primary_culture', 'Maïs').title()}"
        ]
        
        for info in user_info:
            elements.append(Paragraph(info, self.styles['Normal']))
            elements.append(Spacer(1, 10))
        
        elements.append(Spacer(1, 30))
        
        # Date de génération
        date_str = f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        elements.append(Paragraph(date_str, self.styles['Normal']))
        
        return elements
    
    def _create_table_of_contents(self) -> List:
        """Crée le sommaire"""
        elements = []
        
        elements.append(Paragraph("Sommaire", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        sections = [
            "1. Informations de l'agriculteur",
            "2. Conditions météorologiques et conseils",
            "3. Plan d'action temporel (30/60/90 jours)",
            "4. Analyse économique",
            "5. Conseils techniques",
            "6. Annexes"
        ]
        
        for section in sections:
            elements.append(Paragraph(section, self.styles['Normal']))
            elements.append(Spacer(1, 8))
        
        return elements
    
    def _create_user_info_section(self, user_data: Dict) -> List:
        """Crée la section informations utilisateur"""
        elements = []
        
        elements.append(Paragraph("1. Informations de l'agriculteur", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        # Tableau des informations
        user_info_data = [
            ['Profil', 'Détails'],
            ['Nom complet', f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}"],
            ['Type d\'exploitation', user_data.get('user_type', 'individuel').title()],
            ['Zone agro-écologique', user_data.get('zone_agro_ecologique', 'Non spécifiée')],
            ['Objectif de production', user_data.get('farming_objective', 'Non spécifié')],
            ['Surface cultivée', f"{user_data.get('land_area', 0)} {user_data.get('land_unit', 'ha')}"],
            ['Expérience agricole', user_data.get('farming_experience', 'Non spécifiée')],
            ['Culture principale', user_data.get('primary_culture', 'Maïs').title()]
        ]
        
        if user_data.get('user_type') == 'cooperative':
            user_info_data.extend([
                ['Nom de la coopérative', user_data.get('cooperative_name', 'Non spécifié')],
                ['Nombre de membres', str(user_data.get('cooperative_members', 0))],
                ['Commune', user_data.get('cooperative_commune', 'Non spécifiée')]
            ])
        
        table = Table(user_info_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_weather_section(self, weather_data: Dict) -> List:
        """Crée la section météo et conseils"""
        elements = []
        
        elements.append(Paragraph("2. Conditions météorologiques et conseils", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        # Conditions actuelles
        conditions = weather_data.get('conditions_actuelles', {})
        elements.append(Paragraph("<b>Conditions actuelles:</b>", self.styles['Normal']))
        elements.append(Spacer(1, 10))
        
        weather_info = [
            f"• Température: {conditions.get('temperature', 'N/A')}",
            f"• Humidité: {conditions.get('humidity', 'N/A')}",
            f"• Précipitations: {conditions.get('precipitation', 'N/A')}",
            f"• Description: {conditions.get('description', 'N/A')}",
            f"• Zone: {conditions.get('zone', 'N/A')}"
        ]
        
        for info in weather_info:
            elements.append(Paragraph(info, self.styles['WeatherStyle']))
        
        elements.append(Spacer(1, 20))
        
        # Conseils agro-météo
        elements.append(Paragraph("<b>Conseils agro-météo:</b>", self.styles['Normal']))
        elements.append(Spacer(1, 10))
        
        conseils = weather_data.get('conseils', [])
        if conseils:
            for conseil in conseils:
                elements.append(Paragraph(f"• {conseil}", self.styles['AdviceStyle']))
        else:
            elements.append(Paragraph("• Aucun conseil spécifique pour le moment", self.styles['AdviceStyle']))
        
        elements.append(Spacer(1, 15))
        
        # Actions immédiates
        actions = weather_data.get('actions_immediates', [])
        if actions:
            elements.append(Paragraph("<b>Actions immédiates recommandées:</b>", self.styles['Normal']))
            elements.append(Spacer(1, 10))
            
            for action in actions:
                elements.append(Paragraph(f"• {action}", self.styles['AdviceStyle']))
        
        return elements
    
    def _create_action_plan_section(self, user_data: Dict, weather_data: Dict = None) -> List:
        """Crée la section plan d'action temporel"""
        elements = []
        
        elements.append(Paragraph("3. Plan d'action temporel (30/60/90 jours)", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        # Générer le plan selon la culture et la saison
        culture = user_data.get('primary_culture', 'mais')
        current_month = datetime.now().month
        
        # Plan pour le maïs
        if culture.lower() == 'mais':
            plan_30 = self._get_mais_30_days_plan(current_month, weather_data)
            plan_60 = self._get_mais_60_days_plan(current_month, weather_data)
            plan_90 = self._get_mais_90_days_plan(current_month, weather_data)
        else:
            # Plan générique pour autres cultures
            plan_30 = ["Préparation du sol", "Achat des intrants", "Planification des semis"]
            plan_60 = ["Semis", "Premier désherbage", "Fertilisation"]
            plan_90 = ["Entretien", "Lutte contre les ravageurs", "Préparation récolte"]
        
        # Tableau du plan d'action
        plan_data = [
            ['Période', 'Actions principales', 'Détails'],
            ['30 jours', '\n'.join(plan_30[:3]), 'Actions de préparation et démarrage'],
            ['60 jours', '\n'.join(plan_60[:3]), 'Actions de croissance et entretien'],
            ['90 jours', '\n'.join(plan_90[:3]), 'Actions de maturation et récolte']
        ]
        
        table = Table(plan_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _get_mais_30_days_plan(self, current_month: int, weather_data: Dict = None) -> List[str]:
        """Génère le plan 30 jours pour le maïs"""
        if current_month in [3, 4, 5]:  # Mars-Mai
            return [
                "Préparation du sol",
                "Achat des semences",
                "Planification des semis",
                "Préparation des engrais"
            ]
        elif current_month in [6, 7, 8]:  # Juin-Août
            return [
                "Premier désherbage",
                "Fertilisation d'entretien",
                "Surveillance des ravageurs",
                "Irrigation si nécessaire"
            ]
        elif current_month in [9, 10, 11]:  # Septembre-Novembre
            return [
                "Préparation de la récolte",
                "Contrôle de la maturité",
                "Organisation du matériel",
                "Planification du séchage"
            ]
        else:  # Décembre-Février
            return [
                "Analyse des résultats",
                "Planification de la saison suivante",
                "Maintenance du matériel",
                "Formation continue"
            ]
    
    def _get_mais_60_days_plan(self, current_month: int, weather_data: Dict = None) -> List[str]:
        """Génère le plan 60 jours pour le maïs"""
        if current_month in [3, 4, 5]:  # Mars-Mai
            return [
                "Semis en ligne",
                "Premier désherbage",
                "Fertilisation de démarrage",
                "Surveillance de l'émergence"
            ]
        elif current_month in [6, 7, 8]:  # Juin-Août
            return [
                "Deuxième désherbage",
                "Fertilisation de couverture",
                "Lutte contre les ravageurs",
                "Irrigation régulière"
            ]
        elif current_month in [9, 10, 11]:  # Septembre-Novembre
            return [
                "Récolte des épis",
                "Séchage au champ",
                "Battage et vannage",
                "Stockage des grains"
            ]
        else:  # Décembre-Février
            return [
                "Commercialisation",
                "Analyse économique",
                "Préparation sol pour saison suivante",
                "Formation et conseils"
            ]
    
    def _get_mais_90_days_plan(self, current_month: int, weather_data: Dict = None) -> List[str]:
        """Génère le plan 90 jours pour le maïs"""
        if current_month in [3, 4, 5]:  # Mars-Mai
            return [
                "Fertilisation de couverture",
                "Lutte contre les ravageurs",
                "Irrigation si nécessaire",
                "Préparation de la récolte"
            ]
        elif current_month in [6, 7, 8]:  # Juin-Août
            return [
                "Récolte des épis",
                "Séchage et conservation",
                "Battage et vannage",
                "Stockage sécurisé"
            ]
        elif current_month in [9, 10, 11]:  # Septembre-Novembre
            return [
                "Commercialisation",
                "Analyse des rendements",
                "Planification saison suivante",
                "Maintenance équipements"
            ]
        else:  # Décembre-Février
            return [
                "Formation continue",
                "Préparation semis",
                "Achat intrants",
                "Planification financière"
            ]
    
    def _create_economic_analysis_section(self, business_data: Dict) -> List:
        """Crée la section analyse économique"""
        elements = []
        
        elements.append(Paragraph("4. Analyse économique", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        # Tableau économique
        economic_data = [
            ['Poste', 'Montant (FCFA)', 'Observations'],
            ['Charges d\'exploitation', business_data.get('operating_costs', 0), 'Intrants, main d\'œuvre'],
            ['Charges de structure', business_data.get('fixed_costs', 0), 'Équipements, location'],
            ['Chiffre d\'affaires prévu', business_data.get('expected_revenue', 0), 'Production estimée'],
            ['Marge brute', business_data.get('gross_margin', 0), 'CA - Charges variables'],
            ['Résultat net', business_data.get('net_result', 0), 'Marge - Charges fixes']
        ]
        
        table = Table(economic_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_technical_advice_section(self, user_data: Dict) -> List:
        """Crée la section conseils techniques"""
        elements = []
        
        elements.append(Paragraph("5. Conseils techniques", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        culture = user_data.get('primary_culture', 'mais')
        
        if culture.lower() == 'mais':
            advice_items = [
                "• Densité de semis : 50-60 000 plants/ha",
                "• Espacement : 80x25 cm",
                "• Profondeur de semis : 3-5 cm",
                "• Fertilisation NPK : 200-300 kg/ha",
                "• Désherbage : 2-3 passages",
                "• Irrigation : 500-800 mm/an",
                "• Lutte contre les ravageurs : surveillance régulière",
                "• Récolte : 90-120 jours après semis"
            ]
        else:
            advice_items = [
                "• Adapter les techniques à votre culture",
                "• Consulter un expert agricole",
                "• Suivre les recommandations locales",
                "• Tenir un registre des opérations"
            ]
        
        for advice in advice_items:
            elements.append(Paragraph(advice, self.styles['AdviceStyle']))
        
        elements.append(Spacer(1, 20))
        
        return elements 

    def _create_diagnosis_cover_page(self, diagnosis_data: Dict) -> List:
        """Crée la page de garde du diagnostic"""
        elements = []
        
        # Titre principal
        title = "🔍 Rapport de Diagnostic Agricole"
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 30))
        
        # Informations du diagnostic
        diagnosis = diagnosis_data.get('diagnosis', {})
        user_info = diagnosis_data.get('user_info', {})
        
        diagnosis_info = [
            f"<b>Date:</b> {user_info.get('date', 'Non spécifiée')}",
            f"<b>Agriculteur:</b> {user_info.get('name', 'Non spécifié')}",
            f"<b>Zone:</b> {user_info.get('zone', 'Non spécifiée')}",
            f"<b>Culture:</b> {diagnosis.get('culture', 'mais').title()}",
            f"<b>Maladie détectée:</b> {diagnosis.get('disease_name', 'Non identifiée')}",
            f"<b>Sévérité:</b> {diagnosis.get('severity', 'Inconnue')}",
            f"<b>Niveau de confiance:</b> {diagnosis.get('confidence', 0):.1%}"
        ]
        
        for info in diagnosis_info:
            elements.append(Paragraph(info, self.styles['Normal']))
            elements.append(Spacer(1, 10))
        
        elements.append(Spacer(1, 30))
        
        # Avertissement
        warning = """
        <b>⚠️ Avertissement important:</b><br/>
        Ce diagnostic est généré automatiquement par AgroBizChat. 
        Il est recommandé de consulter un expert agricole pour confirmation 
        et validation des traitements recommandés.
        """
        elements.append(Paragraph(warning, self.styles['AdviceStyle']))
        
        return elements
    
    def _create_diagnosis_summary(self, diagnosis_data: Dict) -> List:
        """Crée le résumé du diagnostic"""
        elements = []
        
        elements.append(Paragraph("📋 Résumé du Diagnostic", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        diagnosis = diagnosis_data.get('diagnosis', {})
        
        # Informations de base
        summary_data = [
            ['Élément', 'Détail'],
            ['Maladie', diagnosis.get('disease_name', 'Non identifiée')],
            ['Culture', diagnosis.get('culture', 'mais').title()],
            ['Sévérité', diagnosis.get('severity', 'Inconnue')],
            ['Confiance', f"{diagnosis.get('confidence', 0):.1%}"],
            ['Date du diagnostic', diagnosis_data.get('user_info', {}).get('date', 'Non spécifiée')]
        ]
        
        table = Table(summary_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Symptômes observés
        symptoms = diagnosis.get('symptoms', [])
        if symptoms:
            elements.append(Paragraph("<b>Symptômes observés:</b>", self.styles['Normal']))
            elements.append(Spacer(1, 10))
            
            for symptom in symptoms:
                elements.append(Paragraph(f"• {symptom}", self.styles['AdviceStyle']))
            
            elements.append(Spacer(1, 15))
        
        return elements
    
    def _create_photo_analysis_section(self, diagnosis_data: Dict) -> List:
        """Crée la section d'analyse de la photo"""
        elements = []
        
        elements.append(Paragraph("📸 Analyse de l'Image", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        # Note sur l'image
        photo_note = """
        <b>Image analysée:</b> La photo a été traitée par notre système d'IA 
        pour identifier les symptômes de maladie. L'analyse est basée sur 
        une base de données de maladies agricoles validées.
        """
        elements.append(Paragraph(photo_note, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Détails techniques de l'analyse
        diagnosis = diagnosis_data.get('diagnosis', {})
        
        analysis_data = [
            ['Paramètre', 'Valeur'],
            ['Algorithme utilisé', 'PlantVillage AI'],
            ['Précision détection', f"{diagnosis.get('confidence', 0):.1%}"],
            ['Temps d\'analyse', '< 30 secondes'],
            ['Qualité image', 'Optimisée automatiquement']
        ]
        
        table = Table(analysis_data, colWidths=[2.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_treatments_section(self, diagnosis_data: Dict) -> List:
        """Crée la section des traitements recommandés"""
        elements = []
        
        elements.append(Paragraph("💊 Traitements Recommandés", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        diagnosis = diagnosis_data.get('diagnosis', {})
        treatments = diagnosis.get('treatments', [])
        
        if treatments:
            for i, treatment in enumerate(treatments, 1):
                # Titre du traitement
                treatment_title = f"<b>Traitement {i}: {treatment.get('name', 'Traitement')}</b>"
                elements.append(Paragraph(treatment_title, self.styles['Normal']))
                elements.append(Spacer(1, 5))
                
                # Description
                description = treatment.get('description', '')
                elements.append(Paragraph(f"<b>Description:</b> {description}", self.styles['AdviceStyle']))
                
                # Produits
                products = treatment.get('products', [])
                if products:
                    products_text = "<b>Produits recommandés:</b> " + ", ".join(products)
                    elements.append(Paragraph(products_text, self.styles['AdviceStyle']))
                
                # Application
                application = treatment.get('application', '')
                if application:
                    elements.append(Paragraph(f"<b>Mode d'application:</b> {application}", self.styles['AdviceStyle']))
                
                elements.append(Spacer(1, 15))
        else:
            elements.append(Paragraph("Aucun traitement spécifique recommandé pour le moment.", self.styles['AdviceStyle']))
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("Consultez un expert agricole pour des conseils personnalisés.", self.styles['AdviceStyle']))
        
        return elements
    
    def _create_prevention_section(self, diagnosis_data: Dict) -> List:
        """Crée la section des mesures de prévention"""
        elements = []
        
        elements.append(Paragraph("🛡️ Mesures de Prévention", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        diagnosis = diagnosis_data.get('diagnosis', {})
        prevention = diagnosis.get('prevention', [])
        
        if prevention:
            elements.append(Paragraph("<b>Actions préventives recommandées:</b>", self.styles['Normal']))
            elements.append(Spacer(1, 10))
            
            for measure in prevention:
                elements.append(Paragraph(f"• {measure}", self.styles['AdviceStyle']))
            
            elements.append(Spacer(1, 20))
        
        # Conseils généraux
        general_advice = """
        <b>Conseils généraux de prévention:</b><br/>
        • Surveillez régulièrement vos cultures<br/>
        • Maintenez une bonne hygiène des outils<br/>
        • Évitez la monoculture<br/>
        • Utilisez des variétés résistantes<br/>
        • Adoptez des pratiques culturales appropriées<br/>
        • Consultez régulièrement un expert agricole
        """
        elements.append(Paragraph(general_advice, self.styles['AdviceStyle']))
        
        elements.append(Spacer(1, 20))
        
        # Contact expert
        expert_contact = """
        <b>📞 Contactez un expert:</b><br/>
        Pour un diagnostic plus précis et des conseils personnalisés, 
        contactez un expert agricole ou un technicien agricole local.
        """
        elements.append(Paragraph(expert_contact, self.styles['AdviceStyle']))
        
        return elements 