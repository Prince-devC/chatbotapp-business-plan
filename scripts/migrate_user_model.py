#!/usr/bin/env python3
"""
Script de migration pour enrichir le modèle User
Ajoute les nouveaux champs agricoles au modèle existant
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app, db
from src.models.database import User
from sqlalchemy import text

def migrate_user_model():
    """Migre le modèle User avec les nouveaux champs agricoles"""
    
    with app.app_context():
        try:
            # Vérifier si les colonnes existent déjà
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('users')]
            
            print("Colonnes existantes:", existing_columns)
            
            # Liste des nouveaux champs à ajouter
            new_fields = [
                'user_type',
                'gender', 
                'zone_agro_ecologique',
                'farming_objective',
                'land_unit',
                'land_area',
                'farming_experience',
                'primary_culture',
                'cooperative_name',
                'cooperative_members',
                'cooperative_commune'
            ]
            
            # Ajouter les colonnes manquantes
            for field in new_fields:
                if field not in existing_columns:
                    print(f"Ajout de la colonne: {field}")
                    
                    if field in ['land_area', 'cooperative_members']:
                        # Champs numériques
                        db.engine.execute(text(f"ALTER TABLE users ADD COLUMN {field} FLOAT"))
                    elif field in ['user_type', 'gender', 'land_unit', 'farming_experience', 'primary_culture']:
                        # Champs texte courts
                        db.engine.execute(text(f"ALTER TABLE users ADD COLUMN {field} VARCHAR(50)"))
                    elif field in ['zone_agro_ecologique', 'farming_objective', 'cooperative_commune']:
                        # Champs texte moyens
                        db.engine.execute(text(f"ALTER TABLE users ADD COLUMN {field} VARCHAR(100)"))
                    elif field == 'cooperative_name':
                        # Champ texte long
                        db.engine.execute(text(f"ALTER TABLE users ADD COLUMN {field} VARCHAR(200)"))
                    else:
                        # Par défaut, champ texte
                        db.engine.execute(text(f"ALTER TABLE users ADD COLUMN {field} VARCHAR(100)"))
                    
                    print(f"✅ Colonne {field} ajoutée avec succès")
                else:
                    print(f"⏭️ Colonne {field} existe déjà")
            
            # Mettre à jour les valeurs par défaut
            print("\nMise à jour des valeurs par défaut...")
            db.engine.execute(text("UPDATE users SET user_type = 'individuel' WHERE user_type IS NULL"))
            db.engine.execute(text("UPDATE users SET land_unit = 'ha' WHERE land_unit IS NULL"))
            
            print("✅ Migration terminée avec succès!")
            
            # Afficher les statistiques
            total_users = User.query.count()
            print(f"\n📊 Statistiques:")
            print(f"Total utilisateurs: {total_users}")
            
            # Compter les utilisateurs par type
            individuel_count = User.query.filter_by(user_type='individuel').count()
            cooperative_count = User.query.filter_by(user_type='cooperative').count()
            print(f"Individuels: {individuel_count}")
            print(f"Coopératives: {cooperative_count}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

def create_sample_data():
    """Crée des données d'exemple pour tester"""
    
    with app.app_context():
        try:
            # Créer un utilisateur d'exemple avec profil agricole complet
            sample_user = User(
                platform='whatsapp',
                platform_user_id='test_user_001',
                username='Agriculteur Test',
                first_name='Jean',
                last_name='Dupont',
                phone_number='+22990123456',
                user_type='individuel',
                gender='homme',
                zone_agro_ecologique='Zone des terres de barre',
                farming_objective='commercial',
                land_unit='ha',
                land_area=2.5,
                farming_experience='intermediaire',
                primary_culture='mais',
                is_active=True
            )
            
            db.session.add(sample_user)
            db.session.commit()
            
            print("✅ Utilisateur d'exemple créé avec succès")
            
            # Créer un utilisateur coopérative d'exemple
            cooperative_user = User(
                platform='whatsapp',
                platform_user_id='test_coop_001',
                username='Coopérative Test',
                first_name='Coopérative',
                last_name='Agricole',
                phone_number='+22990123457',
                user_type='cooperative',
                gender='autre',
                zone_agro_ecologique='Zone des collines',
                farming_objective='commercial',
                land_unit='ha',
                land_area=15.0,
                farming_experience='expert',
                primary_culture='mais',
                cooperative_name='Coopérative Agricole du Bénin',
                cooperative_members=25,
                cooperative_commune='Abomey',
                is_active=True
            )
            
            db.session.add(cooperative_user)
            db.session.commit()
            
            print("✅ Coopérative d'exemple créée avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création des données d'exemple: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("🚀 Début de la migration du modèle User...")
    
    # Exécuter la migration
    if migrate_user_model():
        print("\n📝 Création de données d'exemple...")
        create_sample_data()
        print("\n✅ Migration complète terminée!")
    else:
        print("\n❌ Migration échouée!")
        sys.exit(1) 