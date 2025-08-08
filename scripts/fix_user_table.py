#!/usr/bin/env python3
"""
Script pour corriger la table users en ajoutant la colonne user_type manquante
"""

import sqlite3
import os
from pathlib import Path

def fix_user_table():
    """Ajoute la colonne user_type manquante à la table users"""
    
    # Chemin vers la base de données
    project_root = Path(__file__).parent.parent.resolve()
    db_path = project_root / 'database' / 'app.db'
    
    print(f"🔧 Correction de la table users dans: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la colonne user_type existe
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_type' not in columns:
            print("➕ Ajout de la colonne user_type...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN user_type VARCHAR(50) DEFAULT 'regular'
            """)
            conn.commit()
            print("✅ Colonne user_type ajoutée avec succès")
        else:
            print("✅ Colonne user_type existe déjà")
        
        # Vérifier les autres colonnes manquantes
        required_columns = [
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
        
        for column in required_columns:
            if column not in columns:
                print(f"➕ Ajout de la colonne {column}...")
                if column in ['land_area', 'cooperative_members']:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column} INTEGER DEFAULT 0")
                else:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column} VARCHAR(255)")
                conn.commit()
                print(f"✅ Colonne {column} ajoutée")
        
        # Vérifier la structure finale
        cursor.execute("PRAGMA table_info(users)")
        final_columns = [column[1] for column in cursor.fetchall()]
        print(f"\n📋 Structure finale de la table users:")
        for column in final_columns:
            print(f"  - {column}")
        
        conn.close()
        print("\n🎉 Table users corrigée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_user_table() 