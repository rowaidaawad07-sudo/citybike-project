"""
CityBike — Bike-Sharing Analytics Platform
===========================================
Haupt-Einstiegspunkt, der die gesamte Pipeline steuert.
"""

import sys
import os
import numpy as np
from pathlib import Path

# --- Pfad-Konfiguration ---
# Bestimmung des Root-Verzeichnisses des Projekts
BASE_DIR = Path(__file__).parent.absolute()

# Das Root-Verzeichnis zum sys.path hinzufügen, um Paket-Importe zu ermöglichen
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Importe - Die Funktionsnamen wurden an visualization.py angepasst
from citybike.analyzer import BikeShareSystem
from citybike.visualization import (
    plot_trips_per_station, 
    plot_monthly_trend, 
    plot_duration_histogram, 
    plot_duration_by_user_type
)
from citybike.pricing import CasualPricing, MemberPricing
from citybike.numerical import calculate_fares

def main() -> None:
    """Führt die komplette CityBike-Analyse-Pipeline aus."""

    # 1. System initialisieren
    # Erstellt die Instanz für das Analyse-System
    system = BikeShareSystem()

    # Schritt 1 — Daten laden
    print("\n>>> Schritt 1: Daten werden geladen ...")
    system.load_data()

    # Schritt 2 — Daten inspizieren
    print("\n>>> Schritt 2: Daten werden inspiziert ...")
    system.inspect_data()

    # Schritt 3 — Datenbereinigung
    print("\n>>> Schritt 3: Datenbereinigung wird durchgeführt ...")
    system.clean_data()

    # Schritt 4 — Analysen
    print("\n>>> Schritt 4: Analysen werden ausgeführt ...")
    summary = system.total_trips_summary()
    print(f"   Gesamtzahl der Fahrten  : {summary['total_trips']}")
    print(f"   Gesamtdistanz           : {summary['total_distance_km']:.2f} km")
    print(f"   Durchschnittliche Dauer : {summary['avg_duration_min']:.2f} min")

    # Schritt 4b — Umsatzberechnung
    print("\n>>> Schritt 4b: Umsatzberechnung (Vektorisierung) ...")
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

    # Schritt 5 — Visualisierungen (Korrekte Funktionsaufrufe)
    print("\n>>> Schritt 5: Diagramme werden erstellt ...")
    plot_trips_per_station(system.trips, system.stations)
    plot_monthly_trend(system.trips)
    plot_duration_histogram(system.trips)
    plot_duration_by_user_type(system.trips)

    # Schritt 6 — Berichtsexport
    print("\n>>> Schritt 6: Zusammenfassender Bericht wird generiert ...")
    system.generate_summary_report()

    print("\n>>> Analyse abgeschlossen! Die Ergebnisse liegen im Ordner 'citybike/output/'.")

if __name__ == "__main__":
    main()
