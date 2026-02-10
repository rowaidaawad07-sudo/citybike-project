from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class Entity(ABC):
    """Abstrakte Basisklasse für alle Domänenobjekte."""
    
    def __init__(self, entity_id: str):
        if not entity_id or not isinstance(entity_id, str):
            raise ValueError("ID muss ein nicht-leerer String sein")
        self._id = entity_id
        self.created_at = datetime.now()
    
    @property
    def id(self) -> str: 
        return self._id

    @abstractmethod
    def __str__(self) -> str: 
        pass
    
    @abstractmethod
    def __repr__(self) -> str: 
        pass

# --- FAHRRAD MODELLE ---
class Bike(Entity):
    """Repräsentiert ein Fahrrad im Leihsystem."""
    
    VALID_STATUSES = {"available", "in_use", "maintenance"}
    
    def __init__(self, bike_id: str, bike_type: str, status: str = "available"):
        super().__init__(bike_id)
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Ungültiger Status: {status}")
        self.bike_type = bike_type
        self._status = status

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError("Ungültiger Status")
        self._status = value

    def __str__(self) -> str: 
        return f"Bike {self.id} ({self.bike_type})"
    
    def __repr__(self) -> str: 
        return f"Bike(id='{self.id}', type='{self.bike_type}', status='{self.status}')"


class ClassicBike(Bike):
    """Ein klassisches Fahrrad mit Gangschaltung."""
    
    def __init__(self, bike_id: str, gear_count: int = 3, status: str = "available"):
        super().__init__(bike_id, "classic", status)
        if gear_count <= 0:
            raise ValueError("Gangzahl muss positiv sein")
        self.gear_count = gear_count

    def __str__(self) -> str:
        return f"Klassisches Bike {self.id} ({self.gear_count} Gänge)"
    
    def __repr__(self) -> str:
        return f"ClassicBike(id='{self.id}', gears={self.gear_count})"


class ElectricBike(Bike):
    """Ein Elektrofahrrad mit Batterieunterstützung."""
    
    def __init__(self, bike_id: str, battery_level: float = 100.0, 
                 status: str = "available", max_range_km: float = 60.0):
        super().__init__(bike_id, "electric", status)
        if not (0 <= battery_level <= 100):
            raise ValueError("Batteriestand muss zwischen 0 und 100 liegen")
        if max_range_km <= 0:
            raise ValueError("Maximale Reichweite muss positiv sein")
        self.battery_level = battery_level
        self.max_range_km = max_range_km

    def __str__(self) -> str:
        return f"E-Bike {self.id} ({self.battery_level}% Batterie)"
    
    def __repr__(self) -> str:
        return f"ElectricBike(id='{self.id}', battery={self.battery_level}%)"


# --- STATION MODELL ---
class Station(Entity):
    """Repräsentiert eine Fahrradstation im Netzwerk."""
    
    def __init__(self, station_id: str, name: str, capacity: int = 20, 
                 latitude: float = 0.0, longitude: float = 0.0):
        super().__init__(station_id)
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Ungültige Geokoordinaten")
        if capacity <= 0:
            raise ValueError("Kapazität muss positiv sein")
        self.name = name
        self.capacity = capacity
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str: 
        return f"Station {self.name} (Kapazität: {self.capacity})"
    
    def __repr__(self) -> str: 
        return f"Station(id='{self.id}', name='{self.name}', capacity={self.capacity})"


# --- NUTZER MODELLE ---
class User(Entity):
    """Basisklasse für Systembenutzer."""
    
    def __init__(self, user_id: str, name: str, user_type: str, email: str = ""):
        super().__init__(user_id)
        self.name = name
        self.user_type = user_type
        if email and "@" not in email:
            raise ValueError("Ungültige E-Mail-Adresse")
        self.email = email
        
    def __str__(self) -> str: 
        return f"User {self.name} ({self.user_type})"
    
    def __repr__(self) -> str: 
        return f"User(id='{self.id}', name='{self.name}', type='{self.user_type}')"


class CasualUser(User):
    """Ein Gelegenheitsnutzer ohne Abonnement."""
    
    def __init__(self, user_id: str, name: str, email: str = "", 
                 day_pass_count: int = 0):
        super().__init__(user_id, name, "casual", email)
        if day_pass_count < 0:
            raise ValueError("Tagespassanzahl darf nicht negativ sein")
        self.day_pass_count = day_pass_count

    def __str__(self) -> str:
        return f"Gelegenheitsnutzer {self.name} ({self.day_pass_count} Tagespässe)"
    
    def __repr__(self) -> str:
        return f"CasualUser(id='{self.id}', name='{self.name}')"


class MemberUser(User):
    """Ein registriertes Mitglied mit Abonnement."""
    
    VALID_TIERS = {"basic", "premium"}
    
    def __init__(self, user_id: str, name: str, email: str = "", 
                 membership_start: Optional[datetime] = None,
                 membership_end: Optional[datetime] = None, 
                 tier: str = "basic"):
        super().__init__(user_id, name, "member", email)
        self.membership_start = membership_start or datetime.now()
        self.membership_end = membership_end
        if tier not in self.VALID_TIERS:
            raise ValueError(f"Tarif muss einer von {self.VALID_TIERS} sein")
        self.tier = tier
        if membership_end and membership_end < self.membership_start:
            raise ValueError("Mitgliedschaftsende muss nach Start liegen")

    def __str__(self) -> str:
        return f"Mitglied {self.name} (Tarif: {self.tier})"
    
    def __repr__(self) -> str:
        return f"MemberUser(id='{self.id}', name='{self.name}', tier='{self.tier}')"


# --- FAHRT MODELL ---
class Trip:
    """Repräsentiert eine einzelne Fahrradfahrt."""
    
    def __init__(self, trip_id: str, user: User, bike: Bike, 
                 start_station: Station, end_station: Station,
                 start_time: datetime, end_time: datetime, 
                 distance_km: float):
        if distance_km < 0:
            raise ValueError("Distanz darf nicht negativ sein")
        if end_time < start_time:
            raise ValueError("Endzeit muss nach Startzeit liegen")
            
        self.trip_id = trip_id
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = distance_km

    @property
    def duration_minutes(self) -> float:
        """Berechnet die Fahrdauer in Minuten."""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60

    def __str__(self) -> str:
        return f"Fahrt {self.trip_id}: {self.start_station.name} → {self.end_station.name}"
    
    def __repr__(self) -> str:
        return f"Trip(trip_id={self.trip_id!r}, user={self.user.id!r}, bike={self.bike.id!r})"


# --- WARTUNGSMODEL ---
class MaintenanceRecord:
    """Repräsentiert einen Wartungseintrag für ein Fahrrad."""
    
    VALID_TYPES = {
        "tire_repair", "brake_adjustment", "battery_replacement",
        "chain_lubrication", "general_inspection"
    }

    def __init__(self, record_id: str, bike: Bike, date: datetime,
                 maintenance_type: str, cost: float, description: str = ""):
        if maintenance_type not in self.VALID_TYPES:
            raise ValueError(f"Ungültiger Wartungstyp: {maintenance_type}")
        if cost < 0:
            raise ValueError("Kosten dürfen nicht negativ sein")
            
        self.record_id = record_id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = cost
        self.description = description

    def __str__(self) -> str:
        return f"Wartung {self.record_id} für {self.bike.id}"
    
    def __repr__(self) -> str:
        return f"MaintenanceRecord(record_id={self.record_id!r}, bike={self.bike.id!r})"