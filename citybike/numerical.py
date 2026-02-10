"""
NumPy-based numerical computations for the CityBike platform.
"""

import numpy as np
from typing import Dict, Tuple, List, Optional


def station_distance_matrix(
    latitudes: np.ndarray, 
    longitudes: np.ndarray
) -> np.ndarray:
    """
    Berechnet paarweise euklidische Distanzen zwischen Stationen.
    
    Verwendet ein vereinfachtes ebenes Erdmodell:
        d = √((lat₂ - lat₁)² + (lon₂ - lon₁)²)
    
    Args:
        latitudes: 1D-Array von Stations-Breitengraden
        longitudes: 1D-Array von Stations-Längengraden
        
    Returns:
        2D symmetrische Distanzmatrix der Form (n, n)
    """
    # Forme die Arrays für Broadcasting um
    lat1 = latitudes[:, np.newaxis]  # Form (n, 1)
    lat2 = latitudes[np.newaxis, :]  # Form (1, n)
    
    lon1 = longitudes[:, np.newaxis]  # Form (n, 1)
    lon2 = longitudes[np.newaxis, :]  # Form (1, n)
    
    # Berechne quadrierte Differenzen
    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2
    
    # Euklidische Distanz
    distances = np.sqrt(lat_diff**2 + lon_diff**2)
    
    return distances


def trip_duration_stats(durations: np.ndarray) -> Dict[str, float]:
    """
    Berechnet zusammenfassende Statistiken für Fahrtdauern.
    
    Args:
        durations: 1D-Array von Fahrtdauern in Minuten
        
    Returns:
        Dictionary mit Schlüsseln: mean, median, std, p25, p75, p90
    """
    # Entferne NaN-Werte für korrekte Berechnungen
    clean_durations = durations[~np.isnan(durations)]
    
    if len(clean_durations) == 0:
        return {
            "mean": 0.0, "median": 0.0, "std": 0.0,
            "p25": 0.0, "p75": 0.0, "p90": 0.0
        }
    
    return {
        "mean": float(np.mean(clean_durations)),
        "median": float(np.median(clean_durations)),
        "std": float(np.std(clean_durations)),
        "p25": float(np.percentile(clean_durations, 25)),
        "p75": float(np.percentile(clean_durations, 75)),
        "p90": float(np.percentile(clean_durations, 90))
    }


def trip_distance_stats(distances: np.ndarray) -> Dict[str, float]:
    """
    Berechnet zusammenfassende Statistiken für Fahrtdistanzen.
    
    Args:
        distances: 1D-Array von Fahrtdistanzen in km
        
    Returns:
        Dictionary mit Schlüsseln: mean, median, std, p25, p75, p90
    """
    # Entferne NaN-Werte für korrekte Berechnungen
    clean_distances = distances[~np.isnan(distances)]
    
    if len(clean_distances) == 0:
        return {
            "mean": 0.0, "median": 0.0, "std": 0.0,
            "p25": 0.0, "p75": 0.0, "p90": 0.0
        }
    
    return {
        "mean": float(np.mean(clean_distances)),
        "median": float(np.median(clean_distances)),
        "std": float(np.std(clean_distances)),
        "p25": float(np.percentile(clean_distances, 25)),
        "p75": float(np.percentile(clean_distances, 75)),
        "p90": float(np.percentile(clean_distances, 90))
    }


def detect_outliers_zscore(
    values: np.ndarray, 
    threshold: float = 3.0
) -> np.ndarray:
    """
    Identifiziert Ausreißerindizes mit der Z-Score-Methode.
    
    Ein Beobachtungswert ist ein Ausreißer, wenn |z| > threshold.
    
    Args:
        values: 1D-Array von numerischen Werten
        threshold: Z-Score-Grenzwert (Standard 3.0)
        
    Returns:
        Boolean-Array — True wo der Wert ein Ausreißer ist
    """
    # Entferne NaN-Werte für korrekte Berechnung
    mask = ~np.isnan(values)
    clean_values = values[mask]
    
    if len(clean_values) == 0:
        return np.zeros_like(values, dtype=bool)
    
    # Berechne Mittelwert und Standardabweichung
    mean = np.mean(clean_values)
    std = np.std(clean_values)
    
    # Vermeide Division durch Null
    if std == 0:
        return np.zeros_like(values, dtype=bool)
    
    # Berechne Z-Scores
    z_scores = np.abs((values - mean) / std)
    
    # Erkenne Ausreißer
    outliers = z_scores > threshold
    
    # Setze NaN-Werte auf False
    outliers[~mask] = False
    
    return outliers


def calculate_fares(
    durations: np.ndarray,
    distances: np.ndarray,
    per_minute: float,
    per_km: float,
    unlock_fee: float = 0.0,
) -> np.ndarray:
    """
    Berechnet Fahrpreise für viele Fahrten gleichzeitig mit NumPy.
    
    Args:
        durations: 1D-Array von Fahrtdauern (Minuten)
        distances: 1D-Array von Fahrtdistanzen (km)
        per_minute: Kosten pro Minute
        per_km: Kosten pro km
        unlock_fee: Pauschale Entsperrgebühr (Standard 0.0)
        
    Returns:
        1D-Array von Fahrpreisen
    """
    # Vektorisierte Berechnung
    fares = unlock_fee + (per_minute * durations) + (per_km * distances)
    
    # Runde auf 2 Dezimalstellen (Cent-Genauigkeit)
    return np.round(fares, 2)


def calculate_station_utilization(
    trip_counts: np.ndarray,
    station_capacities: np.ndarray,
    time_period_hours: float = 24.0
) -> np.ndarray:
    """
    Berechnet die Auslastung von Stationen.
    
    Args:
        trip_counts: Anzahl der Fahrten pro Station
        station_capacities: Kapazität jeder Station (Anzahl Fahrradplätze)
        time_period_hours: Zeitraum in Stunden (Standard: 24h)
        
    Returns:
        Auslastung in Prozent (0-100)
    """
    # Vermeide Division durch Null
    capacities = np.where(station_capacities == 0, 1, station_capacities)
    
    # Durchschnittliche Auslastung pro Stunde
    avg_trips_per_hour = trip_counts / time_period_hours
    
    # Auslastung in Prozent (angenommen: 1 Trip = 1 Platz für 1 Stunde belegt)
    utilization = (avg_trips_per_hour / capacities) * 100
    
    # Begrenze auf 100%
    return np.minimum(utilization, 100.0)


def compute_correlation_matrix(
    *arrays: np.ndarray,
    column_names: Optional[List[str]] = None
) -> np.ndarray:
    """
    Berechnet die Korrelationsmatrix zwischen mehreren Arrays.
    
    Args:
        *arrays: NumPy-Arrays mit gleicher Länge
        column_names: Optionale Namen für die Arrays/Spalten
        
    Returns:
        Korrelationsmatrix
    """
    if not arrays:
        return np.array([])
    
    # Prüfe, dass alle Arrays die gleiche Länge haben
    lengths = [len(arr) for arr in arrays]
    if len(set(lengths)) > 1:
        raise ValueError("Alle Arrays müssen die gleiche Länge haben")
    
    # Erstelle eine Matrix aus den Arrays
    data_matrix = np.column_stack(arrays)
    
    # Berechne Korrelationsmatrix
    correlation_matrix = np.corrcoef(data_matrix, rowvar=False)
    
    return correlation_matrix


# Beispielverwendung und Tests
if __name__ == "__main__":
    print("🧪 Teste Numerical-Modul...")
    
    # Testdaten
    np.random.seed(42)
    
    # Stationen
    n_stations = 5
    latitudes = np.array([52.52, 52.53, 52.54, 52.55, 52.56])
    longitudes = np.array([13.40, 13.41, 13.42, 13.43, 13.44])
    
    # Fahrten
    n_trips = 100
    durations = np.random.exponential(scale=20, size=n_trips)
    distances = np.random.exponential(scale=5, size=n_trips)
    
    # Teste Distanzmatrix
    print("\n1. Teste Distanzmatrix...")
    dist_matrix = station_distance_matrix(latitudes, longitudes)
    print(f"   Form der Matrix: {dist_matrix.shape}")
    print(f"   Beispiel-Distanz Station 0->1: {dist_matrix[0, 1]:.4f}")
    
    # Teste Statistiken
    print("\n2. Teste Statistiken...")
    duration_stats = trip_duration_stats(durations)
    print(f"   Dauer - Mittelwert: {duration_stats['mean']:.2f} min")
    print(f"   Dauer - Median: {duration_stats['median']:.2f} min")
    
    distance_stats = trip_distance_stats(distances)
    print(f"   Distanz - Mittelwert: {distance_stats['mean']:.2f} km")
    print(f"   Distanz - 90. Perzentil: {distance_stats['p90']:.2f} km")
    
    # Teste Ausreißererkennung
    print("\n3. Teste Ausreißererkennung...")
    # Füge einige Ausreißer hinzu
    test_values = np.concatenate([durations, np.array([500, 600])])  # Zwei extreme Werte
    outliers = detect_outliers_zscore(test_values, threshold=3.0)
    print(f"   Gefundene Ausreißer: {np.sum(outliers)}")
    
    # Teste Fahrpreisberechnung
    print("\n4. Teste Fahrpreisberechnung...")
    fares = calculate_fares(
        durations[:5],  # Erste 5 Fahrten
        distances[:5],
        per_minute=0.15,
        per_km=0.10,
        unlock_fee=1.00
    )
    print(f"   Beispiel-Fahrpreise: {fares}")
    
    # Teste Korrelationsmatrix
    print("\n5. Teste Korrelationsmatrix...")
    corr_matrix = compute_correlation_matrix(durations, distances)
    print(f"   Korrelation Dauer-Distanz: {corr_matrix[0, 1]:.3f}")
    
    print("\n✅ Alle Tests erfolgreich!")