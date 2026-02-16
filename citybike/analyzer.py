"""
CityBike-Analyse-Engine.
Diese Klasse steuert das Laden, Bereinigen und die Auswertung der Daten.
Beantwortet alle 14 Analysefragen des Projekts mit detaillierten Ergebnissen.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Union, Any

# Absolute Pfadkonfiguration für Daten und Berichte
DATA_DIR: Path = Path(__file__).resolve().parent / "data"
OUTPUT_DIR: Path = Path(__file__).resolve().parent / "output"

class BikeShareSystem:
    """Zentrales System zur Analyse der Bike-Sharing-Daten."""

    def __init__(self) -> None:
        """Initialisiert die Datenbehälter für Fahrten, Stationen und Wartung."""
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    def load_data(self) -> None:
        """Schritt 1: Lädt die Rohdaten aus den CSV-Dateien."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

    def inspect_data(self) -> None:
        """Schritt 2: Überprüft die Datenstruktur und identifiziert fehlende Werte."""
        for name, df in [("Trips", self.trips), ("Stations", self.stations), ("Maintenance", self.maintenance)]:
            if df is not None:
                print(f"\n========================================")
                print(f"   {name} Inspektion")
                print(f"========================================")
                print(df.info())
                print("\nFehlende Werte (Null-Werte):")
                print(df.isnull().sum())

    def clean_data(self) -> None:
        """Schritt 3: Datenbereinigung und Typkonvertierung."""
        if self.trips is None: return

        # Entfernen von Duplikaten basierend auf der Trip-ID
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])

        # Datumsformate in datetime-Objekte umwandeln
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"])
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"])

        # Behandlung von Ausreißern und fehlerhaften Werten in Dauer und Distanz
        self.trips["duration_minutes"] = pd.to_numeric(self.trips["duration_minutes"], errors='coerce').fillna(0)
        self.trips["distance_km"] = pd.to_numeric(self.trips["distance_km"], errors='coerce').fillna(0)
        
        if self.maintenance is not None:
            self.maintenance["cost"] = pd.to_numeric(self.maintenance["cost"], errors='coerce').fillna(0.0)

        # Logik-Check: Die Endzeit muss chronologisch nach der Startzeit liegen
        self.trips = self.trips[self.trips["end_time"] >= self.trips["start_time"]]
        print(f"Bereinigung abgeschlossen. Verbleibende Datensätze: {len(self.trips)}")

        # -------------------------------------------------------------------------
        # UNIT 11: Export der bereinigten Daten 
        # -------------------------------------------------------------------------
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Sicherstellen, dass Ordner existiert
        cleaned_file_path = OUTPUT_DIR / "trips_cleaned.csv"
        
        # Der finale Export-Schritt 
        self.trips.to_csv(cleaned_file_path, index=False) # <--- HIER wird die Datei gespeichert

    # ------------------------------------------------------------------
    # ANALYTICS - DIE 14 FRAGEN
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> Dict[str, Any]:
        """Q1: Berechnung der Kernstatistiken (Anzahl, Distanz, Dauer)."""
        return {
            "total_trips": len(self.trips),
            "total_distance_km": round(self.trips["distance_km"].sum(), 2),
            "avg_duration_min": round(self.trips["duration_minutes"].mean(), 2),
        }

    def get_top_10_stations(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Q2: Ermittlung der 10 meistgenutzten Start- und Endstationen."""
        # Top 10 Startstationen ermitteln und mit Stationsnamen zusammenführen
        s_counts = self.trips["start_station_id"].value_counts().head(10).reset_index()
        s_counts.columns = ["station_id", "trip_count"]
        top_start = pd.merge(s_counts, self.stations[["station_id", "station_name"]], on="station_id")

        # Top 10 Endstationen ermitteln und mit Stationsnamen zusammenführen
        e_counts = self.trips["end_station_id"].value_counts().head(10).reset_index()
        e_counts.columns = ["station_id", "trip_count"]
        top_end = pd.merge(e_counts, self.stations[["station_id", "station_name"]], on="station_id")
        
        return top_start, top_end

    def peak_usage_hours(self) -> pd.Series: 
        """Q3: Analyse der Spitzenzeiten nach Tagesstunde."""
        return self.trips["start_time"].dt.hour.value_counts().sort_index()

    def busiest_days(self) -> pd.Series: 
        """Q4: Ermittlung der belebtesten Wochentage."""
        return self.trips["start_time"].dt.day_name().value_counts()

    def avg_dist_user_type(self) -> pd.Series: 
        """Q5: Durchschnittliche Distanz basierend auf dem Nutzertyp."""
        return self.trips.groupby("user_type")["distance_km"].mean()

    def bike_utilization(self) -> pd.Series:
        """
        Q6: Berechnet die Auslastungsrate in Prozent.
        Diese Funktion berechnet, wie viel Prozent der Gesamtzeit jedes Fahrrad im Einsatz war.
        """
        # 1. Berechnung des gesamten Zeitraums in Minuten (Maximalzeit minus Minimalzeit)
        total_period_min = (self.trips["start_time"].max() - self.trips["start_time"].min()).total_seconds() / 60
        
        # 2. Summierung der Nutzungsminuten für jedes einzelne Fahrrad (bike_id)
        usage_per_bike = self.trips.groupby("bike_id")["duration_minutes"].sum()
        
        # 3. Berechnung der Rate: (Nutzungszeit / Gesamtzeit) * 100 für Prozentwerte
        utilization_rate = (usage_per_bike / total_period_min) * 100
        
        # Rückgabe der 10 Fahrräder mit der höchsten Auslastung
        return utilization_rate.sort_values(ascending=False).head(10)

    def monthly_trend(self) -> pd.Series: 
        """Q7: Monatlicher Trend der Fahrtenzahlen über den Zeitverlauf."""
        return self.trips.set_index("start_time").resample("ME").size()

    def maint_cost_by_type(self) -> pd.Series: 
        """Q8: Summierte Wartungskosten aufgeteilt nach Fahrradtyp."""
        return self.maintenance.groupby("bike_type")["cost"].sum()

    def active_users(self) -> pd.Series: 
        """Q9: Identifikation der Top 10 aktivsten Nutzer."""
        return self.trips["user_id"].value_counts().head(10)

    def popular_routes(self) -> pd.DataFrame: 
        """Q10: Ermittlung der 10 am häufigsten befahrenen Routen (Start-End-Kombination)."""
        # تم استخدام reset_index لضمان ظهور أسماء المحطات في التقرير بشكل كامل
        return self.trips.groupby(["start_station_id", "end_station_id"]).size().sort_values(ascending=False).head(10).reset_index(name='trips')

    def trip_status_dist(self) -> pd.Series: 
        """Q11: Verteilung des Fahrtstatus (z.B. abgeschlossen, abgebrochen)."""
        return self.trips["status"].value_counts()

    def user_segment_avg(self) -> pd.Series: 
        """Q12: Durchschnittliche Fahrtenanzahl pro Nutzer innerhalb der Segmente."""
        return self.trips.groupby(["user_type", "user_id"]).size().groupby("user_type").mean()

    def maintenance_freq(self) -> pd.Series: 
        """Q13: Top 10 Fahrräder mit der höchsten Wartungsfrequenz."""
        return self.maintenance["bike_id"].value_counts().head(10)

    def statistical_outliers(self) -> pd.DataFrame: 
        """Q14: Identifikation von statistischen Ausreißern (Dauer > 3 Standardabweichungen)."""
        m, s = self.trips["duration_minutes"].mean(), self.trips["duration_minutes"].std()
        return self.trips[self.trips["duration_minutes"] > (m + 3 * s)]

    # ------------------------------------------------------------------
    # DETAILLIERTE BERICHTSGENERIERUNG
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """
        Erzeugt einen umfassenden Analysebericht im Textformat.
        Alle Kommentare und Analysen sind auf Deutsch verfasst.
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        # --- DATENVORBEREITUNG ---
        s = self.total_trips_summary()
        t_start, t_end = self.get_top_10_stations()

        # --- Q6: BIKE-AUSLASTUNG FORMATIERUNG ---
        bike_stats = self.bike_utilization()
        bike_format = "\n".join([f"   {bid:<10} {val:>8.2f}%" for bid, val in bike_stats.items()])

        # --- Q7: TREND-ANALYSE (DYNAMISCH) ---
        monthly_data = self.monthly_trend()
        top_month = monthly_data.idxmax().strftime('%B')
        top_val = monthly_data.max()
        growth = ((monthly_data.iloc[-1] - monthly_data.iloc[0]) / monthly_data.iloc[0]) * 100
        
        status = "ein Wachstum" if growth > 5 else "einen Rückgang" if growth < -5 else "eine stabile Nutzung"
        trend_comment = (
            f"ANALYSE: Die Daten zeigen {status} im Vergleich zum Jahresbeginn ({growth:.1f}%). "
            f"Der aktivste Monat war der {top_month} mit {top_val} Fahrten."
        )

        # --- Q9: AKTIVSTE NUTZER ANALYSE ---
        top_users = self.active_users().head(15)
        user_comment = (
            f"ANALYSE: Der Nutzer '{top_users.index[0]}' ist mit {top_users.iloc[0]} Fahrten am aktivsten. "
            f"Diese Top 15 Power-User bilden den Kern der Systemnutzung."
        )
        
        # --- Q10: ROUTEN ---
        routes = self.popular_routes()

        # --- BERICHTSAUFBAU ---
        lines = [
            "============================================================",
            "         CITYBIKE — DETAILLIERTER ANALYSEBERICHT",
            "============================================================",
            "\nPROZESS-DETAILS:",
            "Die Daten wurden erfolgreich bereinigt. Ausreißer wurden identifiziert.",
            "Hier sind die detaillierten Ergebnisse der 14 Analysefragen:",
            
            f"\n[1] GESAMTSTATISTIK:",
            f"    - Gesamtzahl valider Fahrten: {s['total_trips']}",
            f"    - Gesamte Distanz: {s['total_distance_km']:.2f} km",
            f"    - Durchschnittliche Dauer: {s['avg_duration_min']:.2f} Minuten",
            
            f"\n[2a] TOP 10 STARTSTATIONEN:\n{t_start.to_string(index=False)}",
            f"\n[2b] TOP 10 ENDSTATIONEN:\n{t_end.to_string(index=False)}",
            f"\n[3] NUTZUNG NACH STUNDEN (PEAK HOURS):\n{self.peak_usage_hours().to_string()}",
            f"\n[4] WOCHENTAG-ANALYSE:\n{self.busiest_days().to_string()}",
            f"\n[5] DISTANZ PRO NUTZERTYP:\n{self.avg_dist_user_type().to_string()}",
            
            f"\n[6] TOP 10 BIKE-ID AUSLASTUNG (IN %):\n{bike_format}",
            
            f"\n[7] MONATLICHER TREND:\n{monthly_data.to_string()}",
            trend_comment,
            
            f"\n[8] WARTUNGSKOSTEN NACH TYP:\n{self.maint_cost_by_type().to_string()}",
            
            f"\n[9] TOP 15 AKTIVSTE NUTZER:\n{top_users.to_string()}",
            user_comment,
            
            f"\n[10] TOP 10 BELIEBTESTE ROUTEN:\n{routes.to_string(index=False)}",
            f"\n[11] FAHRTSTATUS-VERTEILUNG:\n{self.trip_status_dist().to_string()}",
            f"\n[12] DURCHSCHNITTSRATE PRO SEGMENT:\n{self.user_segment_avg().to_string()}",
            f"\n[13] TOP 10 WARTUNGS-FREQUENZ (BIKE-ID):\n{self.maintenance_freq().to_string()}",
            f"\n[14] STATISTISCHE AUSREISSER (TOP 10 LÄNGSTE FAHRTEN):\n" + 
            f"{self.statistical_outliers()[['trip_id', 'duration_minutes']].head(10).to_string(index=False)}",
            
            "\n" + "=" * 60,
            "                                ENDE DES BERICHTS",
            "=" * 60
        ]

        # --- SPEICHERN ---
        report_path.write_text("\n".join(lines), encoding='utf-8')
        print(f"Bericht wurde unter {report_path} gespeichert.")