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

# --- Pfad-Konfiguration für Module und Daten ---
# Wir definieren das Hauptverzeichnis (Root) des Projekts
BASE_DIR = Path(__file__).parent.absolute()

# Das Hauptverzeichnis zum sys.path hinzufügen, damit 'citybike' als Package erkannt wird
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Importe aus dem 'citybike' Package
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
    # Das System-Objekt wird erstellt (nutzt Pfade innerhalb von citybike/)
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

    # Schritt 4 — Analysen und Statistiken
    print("\n>>> Schritt 4: Analysen werden ausgeführt ...")
    summary = system.total_trips_summary()
    print(f"   Gesamtzahl der Fahrten  : {summary['total_trips']}")
    print(f"   Gesamtdistanz           : {summary['total_distance_km']:.2f} km")
    print(f"   Durchschnittliche Dauer : {summary['avg_duration_min']:.2f} min")

    # Schritt 4b — Umsatzberechnung mit NumPy
    print("\n>>> Schritt 4b: Umsatzberechnung (Vektorisierung) ...")
    casual_strat = CasualPricing()
    
    # Filter für Casual-Nutzer anwenden
    casual_mask = system.trips["user_type"] == "casual"
    if any(casual_mask):
        durations = system.trips.loc[casual_mask, "duration_minutes"].to_numpy()
        distances = system.trips.loc[casual_mask, "distance_km"].to_numpy()
        
        # Berechnung der Gebühren
        fares = calculate_fares(
            durations=durations,
            distances=distances,
            per_minute=casual_strat.PER_MINUTE,
            per_km=casual_strat.PER_KM,
            unlock_fee=casual_strat.UNLOCK_FEE
        )
        print(f"   Gesamtumsatz (Casual)   : €{np.sum(fares):.2f}")

    # Schritt 5 — Visualisierungen (Plots)
    print("\n>>> Schritt 5: Diagramme werden erstellt ...")
    # Diese Funktionen speichern die Bilder in 'citybike/output/figures/'
    create_trips_per_station_chart(system.trips, system.stations)
    create_monthly_trend_chart(system.trips)
    create_duration_histogram(system.trips)
    create_duration_boxplot(system.trips)

    # Schritt 6 — Berichtsexport
    print("\n>>> Schritt 6: Zusammenfassender Bericht wird generiert ...")
    system.generate_summary_report()

    print("\n>>> Analyse abgeschlossen! Die Ergebnisse liegen im Ordner 'citybike/output/'.")

if __name__ == "__main__":
    main()