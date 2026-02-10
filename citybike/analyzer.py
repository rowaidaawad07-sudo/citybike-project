"""
Data analysis engine for the CityBike platform.
Enthält die BikeShareSystem-Klasse, die das Laden, Bereinigen und Analysieren der Daten koordiniert.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


class BikeShareSystem:
    """Zentrale Analyseklasse — lädt, bereinigt und analysiert Bike-Sharing-Daten."""

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Daten laden
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Lädt Roh-CSV-Dateien in DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")
        print(f"✅ Geladene Fahrten: {len(self.trips)}")

    # ------------------------------------------------------------------
    # Dateninspektion
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Zeigt grundlegende Informationen zu jedem DataFrame."""
        for name, df in [("Fahrten", self.trips), ("Stationen", self.stations), ("Wartungen", self.maintenance)]:
            print(f"\n🔍 {name} Info:")
            print(df.info())
            print(f"\nFehlende Werte:\n{df.isnull().sum()}")

    # ------------------------------------------------------------------
    # Datenbereinigung
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        """Bereinigt alle DataFrames und exportiert sie als CSV."""
        if self.trips is None:
            raise RuntimeError("Rufen Sie zuerst load_data() auf")

        # 1. Duplikate entfernen
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        self.stations = self.stations.drop_duplicates(subset=["station_id"])
        self.maintenance = self.maintenance.drop_duplicates(subset=["record_id"])

        # 2. Datumswerte parsen
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"])
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"])
        self.maintenance["date"] = pd.to_datetime(self.maintenance["date"])

        # 3. Numerische Spalten konvertieren
        self.trips["duration_minutes"] = pd.to_numeric(self.trips["duration_minutes"], errors='coerce')
        self.trips["distance_km"] = pd.to_numeric(self.trips["distance_km"], errors='coerce')
        self.maintenance["cost"] = pd.to_numeric(self.maintenance["cost"], errors='coerce')

        # 4. Fehlende Werte behandeln (Strategie: Median-Imputation)
        self.trips["duration_minutes"] = self.trips["duration_minutes"].fillna(self.trips["duration_minutes"].median())
        self.trips["distance_km"] = self.trips["distance_km"].fillna(self.trips["distance_km"].median())
        self.maintenance["cost"] = self.maintenance["cost"].fillna(self.maintenance["cost"].median())

        # 5. Ungültige Einträge entfernen (end_time muss nach start_time liegen)
        self.trips = self.trips[self.trips["end_time"] >= self.trips["start_time"]].copy()

        # 6. Kategorische Werte standardisieren
        self.trips["user_type"] = self.trips["user_type"].str.lower().str.strip()
        self.trips["status"] = self.trips["status"].str.lower().str.strip()
        self.trips["bike_type"] = self.trips["bike_type"].str.lower().str.strip()

        # 7. Bereinigte Daten exportieren
        OUTPUT_DIR.mkdir(exist_ok=True)
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)
        self.maintenance.to_csv(DATA_DIR / "maintenance_clean.csv", index=False)
        print("✅ Datenbereinigung und Export abgeschlossen.")

    # ------------------------------------------------------------------
    # Analytics — Geschäftsfragen
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> Dict[str, Any]:
        """Q1: Gesamtzahl der Fahrten, Gesamtdistanz, durchschnittliche Dauer."""
        return {
            "total_trips": len(self.trips),
            "total_distance_km": round(self.trips["distance_km"].sum(), 2),
            "avg_duration_min": round(self.trips["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        """Q2: Top n Startstationen nach Fahrtanzahl."""
        counts = self.trips["start_station_id"].value_counts().head(n).reset_index()
        counts.columns = ["station_id", "trip_count"]
        return pd.merge(counts, self.stations[["station_id", "station_name"]], on="station_id")

    def peak_usage_hours(self) -> pd.Series:
        """Q3: Fahrtanzahl pro Stunde des Tages."""
        return self.trips["start_time"].dt.hour.value_counts().sort_index()

    def busiest_day_of_week(self) -> pd.Series:
        """Q4: Fahrtanzahl pro Wochentag."""
        return self.trips["start_time"].dt.day_name().value_counts()

    def avg_distance_by_user_type(self) -> pd.Series:
        """Q5: Durchschnittliche Distanz nach Benutzertyp."""
        return self.trips.groupby("user_type")["distance_km"].mean()

    def bike_utilization_rate(self) -> float:
        """Q6: Fahrradauslastung (prozentuale Nutzungszeit)."""
        total_trip_minutes = self.trips["duration_minutes"].sum()
        total_bike_minutes = 100 * 30 * 24 * 60  # 100 Räder × 30 Tage × 24h × 60min
        utilization = (total_trip_minutes / total_bike_minutes) * 100
        return round(utilization, 2)

    def monthly_trip_trend(self) -> pd.Series:
        """Q7: Monatliche Fahrtentwicklung über die Zeit."""
        return self.trips.set_index("start_time").resample("M").size()

    def top_active_users(self, n: int = 15) -> pd.Series:
        """Q8: Top n aktivste Nutzer nach Fahrtanzahl."""
        return self.trips["user_id"].value_counts().head(n)

    def maintenance_cost_by_bike_type(self) -> pd.Series:
        """Q9: Gesamte Wartungskosten nach Fahrradtyp."""
        return self.maintenance.groupby("bike_type")["cost"].sum()

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        """Q10: Häufigste Start-Ziel-Stationen-Paare."""
        route_counts = self.trips.groupby(["start_station_id", "end_station_id"]).size().reset_index(name="count")
        top_routes = route_counts.sort_values(by="count", ascending=False).head(n)
        top_routes = pd.merge(top_routes, self.stations[["station_id", "station_name"]], 
                              left_on="start_station_id", right_on="station_id", how="left")
        top_routes = pd.merge(top_routes, self.stations[["station_id", "station_name"]], 
                              left_on="end_station_id", right_on="station_id", 
                              how="left", suffixes=("_start", "_end"))
        return top_routes[["start_station_id", "station_name_start", "end_station_id", "station_name_end", "count"]]

    # Zusätzliche analytische Methoden
    def trip_completion_rate(self) -> float:
        """Q11: Fahrtabschlussrate (abgeschlossen vs. storniert)."""
        if "status" not in self.trips.columns:
            return 0.0
        completed = (self.trips["status"] == "completed").sum()
        total = len(self.trips)
        return round((completed / total) * 100, 2) if total > 0 else 0.0

    def avg_trips_per_user(self) -> pd.Series:
        """Q12: Durchschnittliche Fahrten pro Nutzer, nach Benutzertyp."""
        return self.trips.groupby("user_type")["user_id"].count() / self.trips.groupby("user_type")["user_id"].nunique()

    def bikes_with_most_maintenance(self, n: int = 10) -> pd.Series:
        """Q13: Fahrräder mit den meisten Wartungen."""
        return self.maintenance["bike_id"].value_counts().head(n)

    def identify_outlier_trips(self, threshold: float = 3.0) -> pd.DataFrame:
        """Q14: Identifiziert Ausreißerfahrten basierend auf Dauer und Distanz."""
        duration_z = (self.trips["duration_minutes"] - self.trips["duration_minutes"].mean()) / self.trips["duration_minutes"].std()
        distance_z = (self.trips["distance_km"] - self.trips["distance_km"].mean()) / self.trips["distance_km"].std()
        
        outliers = self.trips[(np.abs(duration_z) > threshold) | (np.abs(distance_z) > threshold)].copy()
        outliers["duration_z_score"] = duration_z
        outliers["distance_z_score"] = distance_z
        return outliers[["trip_id", "user_id", "duration_minutes", "distance_km", "duration_z_score", "distance_z_score"]]

    # ------------------------------------------------------------------
    # Berichterstellung
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """Generiert einen zusammenfassenden Textbericht."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines = ["="*60, "CityBike — Zusammenfassender Bericht", "="*60]
        
        # Q1: Zusammenfassung
        summary = self.total_trips_summary()
        lines.append(f"\n📊 Gesamtzusammenfassung:")
        lines.append(f"  • Fahrten gesamt: {summary['total_trips']}")
        lines.append(f"  • Gesamtdistanz: {summary['total_distance_km']} km")
        lines.append(f"  • Durchschn. Dauer: {summary['avg_duration_min']} min")
        
        # Q2: Top Startstationen
        lines.append(f"\n🏆 Top 5 Startstationen:")
        top_stations = self.top_start_stations(5)
        for _, row in top_stations.iterrows():
            lines.append(f"  • {row['station_name']}: {row['trip_count']} Fahrten")

        # Q3: Spitzenzeiten
        lines.append(f"\n⏰ Top 3 Spitzenstunden:")
        peak_hours = self.peak_usage_hours().head(3)
        for hour, count in peak_hours.items():
            lines.append(f"  • {hour:02d}:00 Uhr: {count} Fahrten")

        # Q4: Beliebster Wochentag
        busiest_day = self.busiest_day_of_week().head(1)
        lines.append(f"\n📅 Beliebtester Wochentag: {busiest_day.index[0]} ({busiest_day.iloc[0]} Fahrten)")

        # Q5: Durchschn. Distanz nach Benutzertyp
        avg_dist = self.avg_distance_by_user_type()
        lines.append("\n🚴 Durchschn. Distanz nach Benutzertyp:")
        for user_type, distance in avg_dist.items():
            lines.append(f"  • {user_type}: {distance:.2f} km")

        # Q6: Auslastungsrate
        lines.append(f"\n📈 Fahrradauslastung: {self.bike_utilization_rate()}%")

        # Q9: Wartungskosten
        maint_costs = self.maintenance_cost_by_bike_type()
        lines.append("\n🔧 Wartungskosten nach Fahrradtyp:")
        for bike_type, cost in maint_costs.items():
            lines.append(f"  • {bike_type}: €{cost:.2f}")

        # Q11: Abschlussrate
        completion_rate = self.trip_completion_rate()
        lines.append(f"\n✅ Fahrtabschlussrate: {completion_rate}%")

        report_path.write_text("\n".join(lines))
        print(f"🚀 Bericht gespeichert unter {report_path}")


# Ausführungslogik
if __name__ == "__main__":
    system = BikeShareSystem()
    try:
        system.load_data()
        system.inspect_data()
        system.clean_data()
        system.generate_summary_report()
    except Exception as e:
        print(f"❌ Fehler: {e}")