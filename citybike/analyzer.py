"""
Modul für Datenverarbeitung und -analyse des Bike-Sharing-Systems.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


class DataLoader:
    """Klasse zum Laden von CSV-Dateien."""
    
    @staticmethod
    def load_trips(filepath: str = "citybike/data/trips.csv") -> pd.DataFrame:
        """
        Lädt die Fahrten-Daten aus einer CSV-Datei.
        
        Args:
            filepath: Pfad zur CSV-Datei
            
        Returns:
            DataFrame mit den Fahrten-Daten
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")
        
        df = pd.read_csv(filepath)
        print(f"✅ Fahrten geladen: {len(df)} Zeilen")
        return df
    
    @staticmethod
    def load_stations(filepath: str = "citybike/data/stations.csv") -> pd.DataFrame:
        """Lädt die Stations-Daten."""
        df = pd.read_csv(filepath)
        print(f"✅ Stationen geladen: {len(df)} Zeilen")
        return df
    
    @staticmethod
    def load_maintenance(filepath: str = "citybike/data/maintenance.csv") -> pd.DataFrame:
        """Lädt die Wartungs-Daten."""
        df = pd.read_csv(filepath)
        print(f"✅ Wartungsdaten geladen: {len(df)} Zeilen")
        return df


class DataCleaner:
    """Klasse zum Bereinigen und Validieren von Daten."""
    
    @staticmethod
    def inspect_data(df: pd.DataFrame, name: str = "Dataset"):
        """
        Untersucht die Struktur und Qualität der Daten.
        
        Args:
            df: DataFrame zur Untersuchung
            name: Name des Datensatzes
        """
        print(f"\n🔍 Untersuchung: {name}")
        print(f"   Zeilen: {df.shape[0]}, Spalten: {df.shape[1]}")
        print(f"   Fehlende Werte gesamt: {df.isnull().sum().sum()}")
        
        # Zeige fehlende Werte pro Spalte
        missing = df.isnull().sum()
        if missing.any():
            print("   Fehlende Werte pro Spalte:")
            for col, count in missing[missing > 0].items():
                percentage = (count / len(df)) * 100
                print(f"     {col}: {count} ({percentage:.1f}%)")
    
    @staticmethod
    def clean_trips(df: pd.DataFrame) -> pd.DataFrame:
        """
        Bereinigt die Fahrten-Daten.
        
        Schritte:
        1. Entfernt Duplikate
        2. Behandelt fehlende Werte
        3. Konvertiert Datentypen
        4. Validiert Zeitstempel
        """
        # Kopie erstellen
        cleaned_df = df.copy()
        
        print("\n🧹 Starte Bereinigung der Fahrten-Daten...")
        
        # 1. Duplikate entfernen
        initial_rows = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        removed = initial_rows - len(cleaned_df)
        print(f"   Duplikate entfernt: {removed}")
        
        # 2. Fehlende Werte behandeln
        # duration_minutes: Mit Median füllen
        if 'duration_minutes' in cleaned_df.columns:
            median_duration = cleaned_df['duration_minutes'].median()
            cleaned_df['duration_minutes'] = cleaned_df['duration_minutes'].fillna(median_duration)
            print(f"   Fehlende Dauer mit Median gefüllt: {median_duration:.1f}")
        
        # distance_km: Mit Mittelwert füllen
        if 'distance_km' in cleaned_df.columns:
            mean_distance = cleaned_df['distance_km'].mean()
            cleaned_df['distance_km'] = cleaned_df['distance_km'].fillna(mean_distance)
            print(f"   Fehlende Entfernung mit Mittelwert gefüllt: {mean_distance:.2f}")
        
        # status: 'completed' annehmen
        if 'status' in cleaned_df.columns:
            cleaned_df['status'] = cleaned_df['status'].fillna('completed')
            print("   Fehlende Status als 'completed' markiert")
        
        # 3. Datentypen konvertieren
        if 'start_time' in cleaned_df.columns:
            cleaned_df['start_time'] = pd.to_datetime(cleaned_df['start_time'], errors='coerce')
        
        if 'end_time' in cleaned_df.columns:
            cleaned_df['end_time'] = pd.to_datetime(cleaned_df['end_time'], errors='coerce')
        
        # 4. Ungültige Zeitstempel entfernen (end_time vor start_time)
        time_mask = cleaned_df['end_time'] < cleaned_df['start_time']
        if time_mask.any():
            invalid_count = time_mask.sum()
            cleaned_df = cleaned_df[~time_mask]
            print(f"   Ungültige Zeitstempel entfernt: {invalid_count}")
        
        print(f"✅ Bereinigung abgeschlossen. Verbleibende Zeilen: {len(cleaned_df)}")
        return cleaned_df