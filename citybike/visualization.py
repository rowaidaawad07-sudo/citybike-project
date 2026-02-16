"""
Matplotlib-Visualisierungen für die CityBike-Plattform.

Erstellt 4 erforderliche Diagramme:
    1. Balkendiagramm — Fahrten pro Station
    2. Liniendiagramm — Monatlicher Trend der Fahrten
    3. Histogramm — Verteilung der Fahrtdauer
    4. Boxplot — Fahrtdauer nach Nutzertyp
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import List

# Pfad für die Ausgabe der Grafiken
FIGURES_DIR: Path = Path(__file__).resolve().parent / "output" / "figures"


def _save_figure(fig: plt.Figure, filename: str) -> None:
    """Speichert eine Matplotlib-Figur im Verzeichnis output/figures/."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    filepath: Path = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Grafik gespeichert: {filepath}")


# ---------------------------------------------------------------------------
# 1. Balkendiagramm (Beispiel)
# ---------------------------------------------------------------------------



def plot_trips_per_station(trips: pd.DataFrame, stations: pd.DataFrame) -> None:
    """Balkendiagramm der 10 meistgenutzten Startstationen."""
    counts: pd.DataFrame = (
        trips["start_station_id"]
        .value_counts()
        .head(10)
        .rename_axis("station_id")
        .reset_index(name="trip_count")
    )
    merged: pd.DataFrame = counts.merge(
        stations[["station_id", "station_name"]],
        on="station_id",
        how="left",
    )

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.barh(merged["station_name"], merged["trip_count"], color="steelblue")
    ax.set_xlabel("Anzahl der Fahrten")
    ax.set_ylabel("Station")
    ax.set_title("Top 10 Startstationen nach Fahrtanzahl")
    ax.invert_yaxis()
    _save_figure(fig, "trips_per_station.png")


# ---------------------------------------------------------------------------
# 2. Liniendiagramm — Monatlicher Trend
# ---------------------------------------------------------------------------



def plot_monthly_trend(trips: pd.DataFrame) -> None:
    """Liniendiagramm des monatlichen Fahrtvolumens."""
    # Sicherstellen, dass start_time ein Datetime-Objekt ist
    trips_copy: pd.DataFrame = trips.copy()
    trips_copy["start_time"] = pd.to_datetime(trips_copy["start_time"])
    
    # Nach Monat gruppieren und zählen
    monthly_counts: pd.Series = trips_copy.set_index("start_time").resample("MS").size()

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(monthly_counts.index, monthly_counts.values, marker='o', linestyle='-', color='darkgreen')
    
    ax.set_xlabel("Monat")
    ax.set_ylabel("Anzahl der Fahrten")
    ax.set_title("Monatlicher Trend des Fahrtvolumens")
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    _save_figure(fig, "monthly_trend.png")


# ---------------------------------------------------------------------------
# 3. Histogramm — Verteilung der Fahrtdauer
# ---------------------------------------------------------------------------



def plot_duration_histogram(trips: pd.DataFrame) -> None:
    """Histogramm der Verteilung von Fahrtdauern."""
    # Filtern von ungültigen Werten
    durations: pd.Series = trips["duration_minutes"].dropna()

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Erstellen des Histogramms mit 30 Bins
    ax.hist(durations, bins=30, color="orange", edgecolor="black", alpha=0.7)
    
    ax.set_xlabel("Fahrtdauer (Minuten)")
    ax.set_ylabel("Häufigkeit")
    ax.set_title("Verteilung der Fahrtdauern")
    ax.grid(True, alpha=0.2)
    
    _save_figure(fig, "duration_histogram.png")


# ---------------------------------------------------------------------------
# 4. Boxplot — Dauer nach Nutzertyp
# ---------------------------------------------------------------------------



def plot_duration_by_user_type(trips: pd.DataFrame) -> None:
    """Boxplot zum Vergleich der Fahrtdauer nach Nutzertyp (Casual vs Member)."""
    # Daten für die verschiedenen Nutzertypen vorbereiten
    data: List[pd.Series] = [
        trips[trips["user_type"] == "casual"]["duration_minutes"].dropna(),
        trips[trips["user_type"] == "member"]["duration_minutes"].dropna()
    ]

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.boxplot(data, labels=["Casual", "Member"], patch_artist=True)
    
    ax.set_ylabel("Fahrtdauer (Minuten)")
    ax.set_title("Vergleich der Fahrtdauer nach Nutzertyp")
    ax.grid(True, axis='y', alpha=0.3)
    
    _save_figure(fig, "duration_by_user_type.png")