"""
Data analysis engine for the CityBike platform.

Contains the BikeShareSystem class that orchestrates:
    - CSV loading and cleaning
    - Answering business questions using Pandas
    - Generating summary reports

Students should implement the cleaning logic and at least 10 analytics methods.
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

class BikeShareSystem:
    """Central analysis class — loads, cleans, and analyzes bike-share data."""

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Load raw CSV files into DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print(f"Loaded trips: {self.trips.shape}")
        print(f"Loaded stations: {self.stations.shape}")
        print(f"Loaded maintenance: {self.maintenance.shape}")

    # ------------------------------------------------------------------
    # Data inspection (provided)
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Print basic info about each DataFrame."""
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            if df is not None:
                print(f"\n{'='*40}")
                print(f"  {name}")
                print(f"{'='*40}")
                print(df.info())
                print(f"\nMissing values:\n{df.isnull().sum()}")
                print(f"\nFirst 3 rows:\n{df.head(3)}")

    # ------------------------------------------------------------------
    # Data cleaning (TODO: Implemented according to steps)
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        """Clean all DataFrames and export to CSV."""
        if self.trips is None:
            raise RuntimeError("Call load_data() first")

        # --- Step 1: Remove duplicates ---
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        print(f"After dedup: {self.trips.shape[0]} trips")

        # --- Step 2: Parse dates ---
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"])
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"])

        # --- Step 3: Convert numeric columns ---
        self.trips["duration_minutes"] = pd.to_numeric(self.trips["duration_minutes"], errors='coerce')
        self.trips["distance_km"] = pd.to_numeric(self.trips["distance_km"], errors='coerce')

        # --- Step 4: Handle missing values ---
        # Strategy: Drop rows with missing critical time info, fill cost with median
        self.trips = self.trips.dropna(subset=["start_time", "end_time", "duration_minutes"])
        if self.maintenance is not None:
            self.maintenance["cost"] = self.maintenance["cost"].fillna(self.maintenance["cost"].median())

        # --- Step 5: Remove invalid entries ---
        self.trips = self.trips[self.trips["end_time"] > self.trips["start_time"]]
        self.trips = self.trips[self.trips["duration_minutes"] > 0]

        # --- Step 6: Standardize categoricals ---
        self.trips["user_type"] = self.trips["user_type"].str.lower().str.strip()

        # --- Step 7: Export cleaned datasets ---
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        if self.stations is not None:
            self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)

        print("Cleaning complete.")

    # ------------------------------------------------------------------
    # Analytics — Business Questions (TODO: Implemented)
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> dict:
        """Q1: Total trips, total distance, average duration."""
        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        """Q2: Top n most popular start stations."""
        counts = self.trips["start_station_id"].value_counts().head(n).reset_index()
        counts.columns = ["station_id", "trip_count"]
        # Merge with station names
        return pd.merge(counts, self.stations[["station_id", "name"]], on="station_id")

    def peak_usage_hours(self) -> pd.Series:
        """Q3: Trip count by hour of day."""
        return self.trips["start_time"].dt.hour.value_counts().sort_index()

    def busiest_day_of_week(self) -> pd.Series:
        """Q4: Trip count by day of week."""
        return self.trips["start_time"].dt.day_name().value_counts()

    def avg_distance_by_user_type(self) -> pd.Series:
        """Q5: Average trip distance grouped by user type."""
        return self.trips.groupby("user_type")["distance_km"].mean()

    def bike_utilization_rate(self) -> pd.Series:
        """Q6: Total trips per bike_id."""
        return self.trips["bike_id"].value_counts()

    def monthly_trip_trend(self) -> pd.Series:
        """Q7: Monthly trip counts over time."""
        return self.trips["start_time"].dt.to_period("M").value_counts().sort_index()

    def top_active_users(self, n: int = 15) -> pd.DataFrame:
        """Q8: Top n most active users by trip count."""
        return self.trips["user_id"].value_counts().head(n)

    def maintenance_cost_by_bike_type(self) -> pd.Series:
        """Q9: Total maintenance cost per bike type."""
        return self.maintenance.groupby("bike_type")["cost"].sum()

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        """Q10: Most common start→end station pairs."""
        return self.trips.groupby(["start_station_id", "end_station_id"]).size().nlargest(n)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """Write a summary text report to output/summary_report.txt."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("   CityBike — Summary Report")
        lines.append("=" * 60)

        # --- Q1: Overall summary ---
        summary = self.total_trips_summary()
        lines.append("\n--- Overall Summary ---")
        lines.append(f"   Total trips       : {summary['total_trips']}")
        lines.append(f"   Total distance    : {summary['total_distance_km']} km")
        lines.append(f"   Avg duration      : {summary['avg_duration_min']} min")

        # --- Q2: Top start stations ---
        top_stations = self.top_start_stations()
        lines.append("\n--- Top 10 Start Stations ---")
        lines.append(top_stations.to_string(index=False))

        # --- Q3: Peak usage hours ---
        hours = self.peak_usage_hours()
        lines.append("\n--- Peak Usage Hours ---")
        lines.append(hours.to_string())

        # --- Q4: Busiest day ---
        lines.append("\n--- Busiest Day of Week ---")
        lines.append(self.busiest_day_of_week().to_string())

        # --- Q9: Maintenance cost by bike type ---
        maint_cost = self.maintenance_cost_by_bike_type()
        lines.append("\n--- Maintenance Cost by Bike Type ---")
        lines.append(maint_cost.to_string())

        # --- Q10: Top Routes ---
        lines.append("\n--- Top 10 Routes ---")
        lines.append(self.top_routes().to_string())

        report_text = "\n".join(lines) + "\n"
        report_path.write_text(report_text)
        print(f"Report saved to {report_path}")
