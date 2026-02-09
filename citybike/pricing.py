"""
Implementierung des Strategy Patterns für Preisstrategien.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class PricingStrategy(ABC):
    """Abstrakte Preisstrategie."""
    
    @abstractmethod
    def calculate_fare(self, duration_minutes: float, distance_km: float, 
                      start_time: datetime = None) -> float:
        """
        Berechnet den Fahrpreis.
        
        Args:
            duration_minutes: Fahrzeit in Minuten
            distance_km: Entfernung in Kilometern
            start_time: Startzeit (optional)
            
        Returns:
            Berechneter Fahrpreis
        """
        pass


class CasualPricing(PricingStrategy):
    """Preisstrategie für Gelegenheitsnutzer."""
    
    def calculate_fare(self, duration_minutes: float, distance_km: float,
                      start_time: datetime = None) -> float:
        # Gelegenheitsnutzer: 5 Basis + 0.5 pro Minute
        base_fare = 5.0
        per_minute = 0.5
        return base_fare + (duration_minutes * per_minute)


class MemberPricing(PricingStrategy):
    """Preisstrategie für Mitglieder."""
    
    def calculate_fare(self, duration_minutes: float, distance_km: float,
                      start_time: datetime = None) -> float:
        # Mitglieder: 2 Basis + 0.2 pro Minute
        base_fare = 2.0
        per_minute = 0.2
        return base_fare + (duration_minutes * per_minute)


class PeakHourPricing(PricingStrategy):
    """Preisstrategie für Stoßzeiten."""
    
    def calculate_fare(self, duration_minutes: float, distance_km: float,
                      start_time: datetime) -> float:
        if not start_time:
            raise ValueError("Startzeit erforderlich für Stoßzeitenpreis")
        
        # Stoßzeiten: 7-9 Uhr und 16-18 Uhr
        if (7 <= start_time.hour <= 9) or (16 <= start_time.hour <= 18):
            multiplier = 1.5
        else:
            multiplier = 1.0
        
        base_fare = 5.0
        per_minute = 0.5
        return (base_fare + (duration_minutes * per_minute)) * multiplier


class DistanceBasedPricing(PricingStrategy):
    """Entfernungsbasierte Preisstrategie."""
    
    def calculate_fare(self, duration_minutes: float, distance_km: float,
                      start_time: datetime = None) -> float:
        # 3 Basis + 0.3 pro Minute + 1.5 pro Kilometer
        base_fare = 3.0
        per_minute = 0.3
        per_km = 1.5
        return base_fare + (duration_minutes * per_minute) + (distance_km * per_km)