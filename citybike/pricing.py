"""
Preisstrategien für die Berechnung der Fahrtkosten (Strategy Pattern).
Bietet ein gemeinsames Interface `PricingStrategy` und konkrete Implementierungen.
"""

from abc import ABC, abstractmethod
from datetime import datetime

# ---------------------------------------------------------------------------
# Strategy interface
# ---------------------------------------------------------------------------

class PricingStrategy(ABC):
    """Abstrakte Preisstrategie — berechnet die Kosten einer Fahrt."""

    @abstractmethod
    def calculate_cost(
        self, duration_minutes: float, distance_km: float, start_time: datetime = None
    ) -> float:
        """
        Gibt die Fahrtkosten in Euro zurück.
        
        Args:
            duration_minutes: Länge der Fahrt in Minuten.
            distance_km: Zurückgelegte Distanz in Kilometern.
            start_time: Startzeitpunkt der Fahrt (wichtig für PeakHourPricing).
        """
        pass


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class CasualPricing(PricingStrategy):
    """
    Preisgestaltung für Gelegenheitsnutzer (Nicht-Mitglieder).
    Tarif:
        - 1.00 € Grundgebühr (Unlock fee)
        - 0.15 € pro Minute
        - 0.10 € pro km
    """

    UNLOCK_FEE = 1.00
    PER_MINUTE = 0.15
    PER_KM = 0.10

    def calculate_cost(
        self, duration_minutes: float, distance_km: float, start_time: datetime = None
    ) -> float:
        return (
            self.UNLOCK_FEE
            + (self.PER_MINUTE * duration_minutes)
            + (self.PER_KM * distance_km)
        )


class MemberPricing(PricingStrategy):
    """
    Preisgestaltung für Mitglieder — vergünstigte Tarife.
    Tarif:
        - Keine Grundgebühr
        - 0.08 € pro Minute
        - 0.05 € pro km
    """

    PER_MINUTE = 0.08
    PER_KM = 0.05

    def calculate_cost(
        self, duration_minutes: float, distance_km: float, start_time: datetime = None
    ) -> float:
        cost = (self.PER_MINUTE * duration_minutes) + (self.PER_KM * distance_km)
        return round(cost, 2)


class PeakHourPricing(PricingStrategy):
    """
    Preisgestaltung während der Stoßzeiten (Aufschlag auf die Casual-Tarife).
    Logik:
        - Wende einen 1.5-fachen Multiplikator auf die CasualPricing-Kosten an.
    """

    MULTIPLIER = 1.5

    def calculate_cost(
        self, duration_minutes: float, distance_km: float, start_time: datetime = None
    ) -> float:
        casual_strategy = CasualPricing()
        base_cost = casual_strategy.calculate_cost(duration_minutes, distance_km)
        
        if start_time:
            # Stoßzeiten: 7-9 Uhr und 16-18 Uhr
            if (7 <= start_time.hour <= 9) or (16 <= start_time.hour <= 18):
                return round(base_cost * self.MULTIPLIER, 2)
            return base_cost
        
        return round(base_cost * self.MULTIPLIER, 2)