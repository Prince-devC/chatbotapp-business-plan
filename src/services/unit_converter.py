"""
Service de conversion d'unités agricoles
"""

class UnitConverter:
    """Service pour convertir les unités agricoles"""
    
    # Facteurs de conversion
    CONVERSION_FACTORS = {
        'canti_to_m2': 400,  # 1 canti = 400 m²
        'canti_to_ha': 0.04,  # 1 canti = 0.04 ha
        'm2_to_ha': 0.0001,   # 1 m² = 0.0001 ha
        'ha_to_m2': 10000,    # 1 ha = 10000 m²
    }
    
    @staticmethod
    def convert_area(value, from_unit, to_unit):
        """
        Convertit une surface d'une unité vers une autre
        
        Args:
            value (float): Valeur à convertir
            from_unit (str): Unité source ('canti', 'm2', 'ha')
            to_unit (str): Unité cible ('m2', 'ha')
            
        Returns:
            float: Valeur convertie
        """
        if from_unit == to_unit:
            return value
            
        # Conversion vers m² d'abord
        if from_unit == 'canti':
            m2_value = value * UnitConverter.CONVERSION_FACTORS['canti_to_m2']
        elif from_unit == 'ha':
            m2_value = value * UnitConverter.CONVERSION_FACTORS['ha_to_m2']
        elif from_unit == 'm2':
            m2_value = value
        else:
            raise ValueError(f"Unité source non reconnue: {from_unit}")
            
        # Conversion de m² vers l'unité cible
        if to_unit == 'm2':
            return m2_value
        elif to_unit == 'ha':
            return m2_value * UnitConverter.CONVERSION_FACTORS['m2_to_ha']
        elif to_unit == 'canti':
            return m2_value / UnitConverter.CONVERSION_FACTORS['canti_to_m2']
        else:
            raise ValueError(f"Unité cible non reconnue: {to_unit}")
    
    @staticmethod
    def get_standard_area(user_area, user_unit):
        """
        Convertit une surface vers les unités standard (ha et m²)
        
        Args:
            user_area (float): Surface de l'utilisateur
            user_unit (str): Unité de l'utilisateur
            
        Returns:
            dict: {'ha': float, 'm2': float}
        """
        if not user_area or not user_unit:
            return {'ha': 0, 'm2': 0}
            
        ha_value = UnitConverter.convert_area(user_area, user_unit, 'ha')
        m2_value = UnitConverter.convert_area(user_area, user_unit, 'm2')
        
        return {
            'ha': round(ha_value, 2),
            'm2': round(m2_value, 0)
        }
    
    @staticmethod
    def format_area_display(area_dict):
        """
        Formate l'affichage d'une surface
        
        Args:
            area_dict (dict): {'ha': float, 'm2': float}
            
        Returns:
            str: Texte formaté
        """
        ha = area_dict.get('ha', 0)
        m2 = area_dict.get('m2', 0)
        
        if ha >= 1:
            return f"{ha} hectare(s) ({m2} m²)"
        else:
            return f"{m2} m²" 