"""
Implementierung des Factory Patterns zur Erstellung von Domänenobjekten.
"""

from typing import Dict, Any
from datetime import datetime
from .models import Bike, ClassicBike, ElectricBike, User, CasualUser, MemberUser, Station


class BikeFactory:
    """Factory zur Erstellung von Bike-Objekten."""
    
    @staticmethod
    def create_bike(data: Dict[str, Any]) -> Bike:
        """
        Erstellt ein Bike-Objekt aus Wörterbuchdaten.
        
        Args:
            data: Wörterbuch mit Fahrraddaten
            
        Returns:
            Entsprechende Bike-Subklasseninstanz
            
        Raises:
            ValueError: Wenn der Fahrradtyp unbekannt ist
        """
        bike_id = data.get('bike_id')
        bike_type = data.get('bike_type', 'classic').lower()
        status = data.get('status', 'available')
        
        if bike_type == 'classic':
            gear_count = int(data.get('gear_count', 3))
            return ClassicBike(bike_id, gear_count, status)
        
        elif bike_type == 'electric':
            battery_level = float(data.get('battery_level', 100.0))
            max_range_km = float(data.get('max_range_km', 60.0))
            return ElectricBike(bike_id, battery_level, max_range_km, status)
        
        else:
            raise ValueError(f"Unbekannter Fahrradtyp: {bike_type}")


class UserFactory:
    """Factory zur Erstellung von User-Objekten."""
    
    @staticmethod
    def create_user(data: Dict[str, Any]) -> User:
        """
        Erstellt ein User-Objekt aus Wörterbuchdaten.
        
        Args:
            data: Wörterbuch mit Benutzerdaten
            
        Returns:
            Entsprechende User-Subklasseninstanz
        """
        user_id = data.get('user_id')
        name = data.get('name', 'Unbekannter Benutzer')
        email = data.get('email', '')
        user_type = data.get('user_type', 'casual').lower()
        
        if user_type == 'casual':
            day_pass_count = int(data.get('day_pass_count', 0))
            return CasualUser(user_id, name, email, day_pass_count)
        
        elif user_type == 'member':
            # Datumsverarbeitung
            start_str = data.get('membership_start')
            end_str = data.get('membership_end')
            
            if isinstance(start_str, str):
                membership_start = datetime.strptime(start_str, '%Y-%m-%d')
            else:
                membership_start = datetime.now()
            
            if isinstance(end_str, str):
                membership_end = datetime.strptime(end_str, '%Y-%m-%d')
            else:
                membership_end = datetime.now()
            
            tier = data.get('tier', 'basic').lower()
            return MemberUser(user_id, name, email, membership_start, membership_end, tier)
        
        else:
            raise ValueError(f"Unbekannter Benutzertyp: {user_type}")


class StationFactory:
    """Factory zur Erstellung von Station-Objekten."""
    
    @staticmethod
    def create_station(data: Dict[str, Any]) -> Station:
        """
        Erstellt ein Station-Objekt aus Wörterbuchdaten.
        
        Args:
            data: Wörterbuch mit Stationsdaten
            
        Returns:
            Station-Instanz
        """
        station_id = data.get('station_id')
        name = data.get('station_name', 'Unbekannte Station')
        capacity = int(data.get('capacity', 10))
        latitude = float(data.get('latitude', 0.0))
        longitude = float(data.get('longitude', 0.0))
        
        return Station(station_id, name, capacity, latitude, longitude)


# Bequemlichkeitsfunktion
def create_entity(entity_type: str, data: Dict[str, Any]):
    """
    Generische Factory-Funktion zur Erstellung beliebiger Entitäten.
    
    Args:
        entity_type: Art der Entität ('bike', 'user', 'station')
        data: Wörterbuch mit Entitätsdaten
        
    Returns:
        Erstelltes Entitätsobjekt
    """
    factories = {
        'bike': BikeFactory(),
        'user': UserFactory(),
        'station': StationFactory()
    }
    
    factory = factories.get(entity_type.lower())
    if not factory:
        raise ValueError(f"Unbekannter Entitätstyp: {entity_type}")
    
    if entity_type == 'bike':
        return factory.create_bike(data)
    elif entity_type == 'user':
        return factory.create_user(data)
    elif entity_type == 'station':
        return factory.create_station(data)