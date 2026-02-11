import pytest
from citybike.models import ClassicBike, ElectricBike
from citybike.factories import create_bike
from citybike.pricing import CasualPricing, MemberPricing
from citybike.analyzer import BikeShareSystem

def test_full_system_flow():
    """
    Integrations-Test: Überprüft, ob alle Systemkomponenten korrekt zusammenarbeiten.
    """
    # 1. Test von Factory und Models
    classic_data = {"bike_id": "C100", "bike_type": "classic", "gear_count": 5}
    bike = create_bike(classic_data)
    assert isinstance(bike, ClassicBike)
    
    # 2. Test der Preisstrategie
    casual_strategy = CasualPricing()
    # نرسل القيم مباشرة كأرقام لتجنب خطأ الأسماء
    price = casual_strategy.calculate_cost(20, 5) 
    
    assert price > 0 
    
    # 3. Test des Analyzers
    system = BikeShareSystem()
    assert system.trips is None

def test_bike_factory_logic():
    """Überprüft die Factory-Logik."""
    electric_data = {
        "bike_id": "E200", 
        "bike_type": "electric", 
        "battery_level": 85.0,
        "max_range_km": 60.0
    }
    bike = create_bike(electric_data)
    assert isinstance(bike, ElectricBike)