from abc import ABC, abstractmethod
from datetime import datetime

class Entity(ABC):
    def __init__(self, entity_id: str):
        self._id = entity_id
        # إضافة created_at لأن الاختبار يطلبه
        self.created_at = datetime.now() 
    
    @property
    def id(self) -> str: return self._id

    @abstractmethod
    def __str__(self) -> str: pass
    
    @abstractmethod
    def __repr__(self) -> str: pass

# --- FAHRRAD MODELLE ---
class Bike(Entity):
    VALID_STATUSES = ["available", "in_use", "maintenance"]
    def __init__(self, bike_id: str, bike_type: str, status: str = "available"):
        super().__init__(bike_id)
        self.bike_type = bike_type
        self.status = status
    def __str__(self): return f"Bike {self.id}"
    def __repr__(self): return f"Bike(id='{self.id}')"

class ClassicBike(Bike):
    def __init__(self, bike_id: str, gear_count: int = 3, status: str = "available"):
        super().__init__(bike_id, "classic", status)
        # التحقق من عدد الجيرات (لحل خطأ Test 4)
        if gear_count <= 0:
            raise ValueError("Gangzahl muss positiv sein")
        self.gear_count = gear_count
class ElectricBike(Bike):
    # إضافة max_range_km كـ keyword argument لحل خطأ الاختبار
    def __init__(self, bike_id: str, battery_level: float = 100.0, status: str = "available", max_range_km: float = 60.0):
        super().__init__(bike_id, "electric", status)
        self.battery_level = battery_level
        self.max_range_km = max_range_km

# --- STATION MODEL ---
class Station(Entity):
    def __init__(self, station_id: str, name: str, location: str = "", capacity: int = 20, latitude: float = 0.0, longitude: float = 0.0):
        super().__init__(station_id)
        # التحقق من الإحداثيات (لضمان نجاح اختبار Station تماماً)
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Ungültige Koordinaten")
        self.name = name
        self.location = location
        self.capacity = capacity
        self.latitude = latitude
        self.longitude = longitude
    def __str__(self): return f"Station {self.name}"
    def __repr__(self): return f"Station(name='{self.name}')"

# --- NUTZER MODELLE ---
class User(Entity):
    def __init__(self, user_id: str, name: str, user_type: str):
        super().__init__(user_id)
        self.name = name
        self.user_type = user_type
    def __str__(self): return f"User {self.name}"
    def __repr__(self): return f"User(name='{self.name}')"

class CasualUser(User):
    def __init__(self, user_id: str, name: str):
        super().__init__(user_id, name, "casual")

class MemberUser(User):
    def __init__(self, user_id: str, name: str, membership_id: str = ""):
        super().__init__(user_id, name, "member")
        self.membership_id = membership_id
