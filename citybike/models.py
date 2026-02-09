"""
Modul, das alle Domänenmodellklassen für das Bike-Sharing-System enthält.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re

class Entity(ABC):
    """
    Abstrakte Basisklasse für alle Entitäten im System.
    
    Attribute:
        id (str): Eindeutiger Bezeichner
        created_at (datetime): Zeitstempel der Erstellung
    """
    
    def __init__(self, entity_id: str):
        """
        Initialisiert eine Entity.
        
        Args:
            entity_id: Eindeutiger Bezeichner für die Entität
        """
        self._id = entity_id
        self._created_at = datetime.now()
    
    @property
    def id(self) -> str:
        """Ruft die Entitäts-ID ab."""
        return self._id
    
    @property
    def created_at(self) -> datetime:
        """Ruft den Erstellungszeitstempel ab."""
        return self._created_at
    
    @abstractmethod
    def __str__(self) -> str:
        """Benutzerfreundliche String-Darstellung."""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """Entwicklerfreundliche String-Darstellung."""
        pass
    
    def __eq__(self, other) -> bool:
        """Überprüft, ob zwei Entitäten die gleiche ID haben."""
        if isinstance(other, Entity):
            return self.id == other.id
        return False


class Bike(Entity):
    """
    Stellt ein Fahrrad im Sharing-System dar.
    
    Attribute:
        bike_id (str): Fahrrad-ID
        bike_type (str): Fahrradtyp (classic/electric)
        status (str): Aktueller Status (available/in_use/maintenance)
    """
    
    # Gültige Statuswerte
    VALID_STATUSES = ["available", "in_use", "maintenance"]
    VALID_TYPES = ["classic", "electric"]
    
    def __init__(self, bike_id: str, bike_type: str, status: str = "available"):
        """
        Initialisiert ein Bike.
        
        Args:
            bike_id: Eindeutige Fahrrad-ID
            bike_type: Fahrradtyp (classic/electric)
            status: Aktueller Status (Standard: available)
        
        Raises:
            ValueError: Wenn bike_type oder status ungültig ist
        """
        super().__init__(bike_id)
        
        # Validierung des Fahrradtyps
        if bike_type not in self.VALID_TYPES:
            raise ValueError(
                f"Ungültiger Fahrradtyp: {bike_type}. "
                f"Muss einer von {self.VALID_TYPES} sein"
            )
        
        # Validierung des Status
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Ungültiger Status: {status}. "
                f"Muss einer von {self.VALID_STATUSES} sein"
            )
        
        self._bike_type = bike_type
        self._status = status
    
    @property
    def bike_id(self) -> str:
        """Ruft die Fahrrad-ID ab."""
        return self.id
    
    @property
    def bike_type(self) -> str:
        """Ruft den Fahrradtyp ab."""
        return self._bike_type
    
    @property
    def status(self) -> str:
        """Ruft den aktuellen Status ab."""
        return self._status
    
    @status.setter
    def status(self, new_status: str):
        """
        Setzt den Fahrradstatus mit Validierung.
        
        Args:
            new_status: Neuer Statuswert
        
        Raises:
            ValueError: Wenn new_status ungültig ist
        """
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Ungültiger Status: {new_status}")
        self._status = new_status
    
    def __str__(self) -> str:
        return f"Fahrrad {self.bike_id} ({self.bike_type}) - {self.status}"
    
    def __repr__(self) -> str:
        return f"Bike(bike_id='{self.bike_id}', bike_type='{self.bike_type}', status='{self.status}')"


class ClassicBike(Bike):
    """
    Stellt ein klassisches (nicht-elektrisches) Fahrrad dar.
    
    Zusätzliches Attribut:
        gear_count (int): Anzahl der Gänge
    """
    
    def __init__(self, bike_id: str, gear_count: int = 3, status: str = "available"):
        """
        Initialisiert ein ClassicBike.
        
        Args:
            bike_id: Eindeutige Fahrrad-ID
            gear_count: Anzahl der Gänge (Standard: 3)
            status: Aktueller Status
        
        Raises:
            ValueError: Wenn gear_count nicht positiv ist
        """
        super().__init__(bike_id, "classic", status)
        
        # Validierung der Gangzahl
        if gear_count <= 0:
            raise ValueError("Gangzahl muss positiv sein")
        
        self._gear_count = gear_count
    
    @property
    def gear_count(self) -> int:
        """Ruft die Anzahl der Gänge ab."""
        return self._gear_count
    
    def __str__(self) -> str:
        return f"Klassisches Fahrrad {self.bike_id} ({self.gear_count} Gänge) - {self.status}"
    
    def __repr__(self) -> str:
        return f"ClassicBike(bike_id='{self.bike_id}', gear_count={self.gear_count}, status='{self.status}')"


class ElectricBike(Bike):
    """
    Stellt ein elektrisches Fahrrad dar.
    
    Zusätzliche Attribute:
        battery_level (float): Aktueller Batteriestand (0-100%)
        max_range_km (float): Maximale Reichweite bei voller Ladung
    """
    
    def __init__(self, bike_id: str, battery_level: float = 100.0, 
                 max_range_km: float = 60.0, status: str = "available"):
        """
        Initialisiert ein ElectricBike.
        
        Args:
            bike_id: Eindeutige Fahrrad-ID
            battery_level: Aktueller Batteriestand (0-100)
            max_range_km: Maximale Reichweite in Kilometern
            status: Aktueller Status
        
        Raises:
            ValueError: Wenn battery_level oder max_range_km ungültig ist
        """
        super().__init__(bike_id, "electric", status)
        
        # Validierung des Batteriestands
        if not 0 <= battery_level <= 100:
            raise ValueError("Batteriestand muss zwischen 0 und 100 liegen")
        
        # Validierung der Reichweite
        if max_range_km <= 0:
            raise ValueError("Maximale Reichweite muss positiv sein")
        
        self._battery_level = battery_level
        self._max_range_km = max_range_km
    
    @property
    def battery_level(self) -> float:
        """Ruft den aktuellen Batteriestand ab."""
        return self._battery_level
    
    @battery_level.setter
    def battery_level(self, level: float):
        """
        Setzt den Batteriestand mit Validierung.
        
        Args:
            level: Neuer Batteriestand (0-100)
        
        Raises:
            ValueError: Wenn level nicht zwischen 0 und 100 liegt
        """
        if not 0 <= level <= 100:
            raise ValueError("Batteriestand muss zwischen 0 und 100 liegen")
        self._battery_level = level
    
    @property
    def max_range_km(self) -> float:
        """Ruft die maximale Reichweite ab."""
        return self._max_range_km
    
    def __str__(self) -> str:
        return f"Elektrofahrrad {self.bike_id} ({self.battery_level}% Batterie) - {self.status}"
    
    def __repr__(self) -> str:
        return (f"ElectricBike(bike_id='{self.bike_id}', "
                f"battery_level={self.battery_level}, "
                f"max_range_km={self.max_range_km}, "
                f"status='{self.status}')")