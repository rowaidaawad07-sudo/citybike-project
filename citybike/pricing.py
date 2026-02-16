"""
Preisstrategien für die Berechnung der Fahrtkosten (Strategy Pattern).

Bietet ein gemeinsames Interface `PricingStrategy` und konkrete Implementierungen.
"""

from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Strategy interface
# ---------------------------------------------------------------------------



class PricingStrategy(ABC):
    """Abstrakte Preisstrategie — berechnet die Kosten einer Fahrt."""

    @abstractmethod
    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Gibt die Fahrtkosten in Euro zurück.

        Args:
            duration_minutes: Länge der Fahrt in Minuten.
            distance_km: Zurückgelegte Distanz in Kilometern.

        Returns:
            Fahrtkosten als Float.
        """
        ...


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class CasualPricing(PricingStrategy):
    """Preisgestaltung für Gelegenheitsnutzer (Nicht-Mitglieder).

    Tarif:
        - 1.00 € Grundgebühr (Unlock fee)
        - 0.15 € pro Minute
        - 0.10 € pro km
    """

    UNLOCK_FEE: float = 1.00
    PER_MINUTE: float = 0.15
    PER_KM: float = 0.10

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Berechnet die Kosten für Casual-Nutzer."""
        cost: float = (
            self.UNLOCK_FEE
            + (self.PER_MINUTE * duration_minutes)
            + (self.PER_KM * distance_km)
        )
        return float(cost)


class MemberPricing(PricingStrategy):
    """Preisgestaltung für Mitglieder — vergünstigte Tarife.

    Tarif:
        - Keine Grundgebühr
        - 0.08 € pro Minute
        - 0.05 € pro km
    """

    PER_MINUTE: float = 0.08
    PER_KM: float = 0.05

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Berechnet die Kosten für Mitglieder ohne Grundgebühr."""
        # Die Formel für Mitglieder: (Kosten pro Min * Dauer) + (Kosten pro km * Distanz)
        cost: float = (self.PER_MINUTE * duration_minutes) + (self.PER_KM * distance_km)
        return float(round(cost, 2))


class PeakHourPricing(PricingStrategy):
    """Preisgestaltung während der Stoßzeiten (Aufschlag auf die Casual-Tarife).

    Logik:
        - Wende einen 1.5-fachen Multiplikator auf die CasualPricing-Kosten an.
    """

    MULTIPLIER: float = 1.5

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Berechnet die Kosten mit einem Stoßzeiten-Aufschlag."""
        # Zuerst die Basis-Kosten für Gelegenheitsnutzer berechnen
        casual_strategy: PricingStrategy = CasualPricing()
        base_cost: float = casual_strategy.calculate_cost(duration_minutes, distance_km)
        
        # Den Multiplikator (1.5x) anwenden
        peak_cost: float = base_cost * self.MULTIPLIER
        return float(round(peak_cost, 2))