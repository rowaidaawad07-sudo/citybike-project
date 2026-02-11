"""
CityBike — Bike-Sharing Analytics Platform
===========================================
Haupt-Einstiegspunkt, der die gesamte Pipeline steuert.

Verwendung:
    python main.py
"""

import sys
import os
import numpy as np
from pathlib import Path

# --- إضافة مسار المجلد لضمان العثور على الموديولات ---
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "citybike"))

# الآن نقوم بالاستيراد من مجلد citybike
from citybike.analyzer import BikeShareSystem
from citybike.visualization import (
    create_trips_per_station_chart, 
    create_monthly_trend_chart, 
    create_duration_histogram, 
    create_duration_boxplot
)
from citybike.pricing import CasualPricing, MemberPricing
from citybike.numerical import calculate_fares

def main() -> None:
    """Führt die komplette CityBike-Analyse-Pipeline aus."""

    # 1. System initialisieren
    # تأكد أن الكلاس يستطيع الوصول لمجلد data من مكانه الجديد
    system = BikeShareSystem()

    # Schritt 1 — Daten laden
    print("\n>>> Daten werden geladen ...")
    system.load_data()

    # Schritt 2 — Daten inspizieren
    print("\n>>> Daten werden inspiziert ...")
    system.inspect_data()

    # Schritt 3 — Daten bereinigen
    print("\n>>> Datenbereinigung wird durchgeführt ...")
    system.clean_data()

    # Schritt 4 — Analysen
    print("\n>>> Analysen werden ausgeführt ...")
    summary = system.total_trips_summary()
    print(f"   Gesamtzahl der Fahrten  : {summary['total_trips']}")
    print(f"   Gesامtdistanz           : {summary['total_distance_km']:.2f} km")
    print(f"   Durchschnittliche Dauer : {summary['avg_duration_min']:.2f} min")

    # Schritt 4b — Preisberechnung
    print("\n>>> Umsatzberechnung mit NumPy-Vektorisierung ...")
    casual_strat = CasualPricing()
    
    casual_mask = system.trips["user_type"] == "casual"
    if any(casual_mask):
        durations = system.trips.loc[casual_mask, "duration_minutes"].to_numpy()
        distances = system.trips.loc[casual_mask, "distance_km"].to_numpy()
        
        fares = calculate_fares(
            durations=durations,
            distances=distances,
            per_minute=casual_strat.PER_MINUTE,
            per_km=casual_strat.PER_KM,
            unlock_fee=casual_strat.UNLOCK_FEE
        )
        print(f"   Gesamtumsatz (Casual)   : €{np.sum(fares):.2f}")

    # Schritt 5 — Visualisierungen
    print("\n>>> Diagramme werden erstellt ...")
    create_trips_per_station_chart(system.trips, system.stations)
    create_monthly_trend_chart(system.trips)
    create_duration_histogram(system.trips)
    create_duration_boxplot(system.trips)

    # Schritt 6 — Bericht exportieren
    print("\n>>> Zusammenfassender Bericht wird erstellt ...")
    system.generate_summary_report()

    print("\n>>> Fertig! Ergebnisse finden Sie im Ordner 'output/'.")

if __name__ == "__main__":
    main()