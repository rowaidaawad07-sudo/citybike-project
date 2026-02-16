"""
NumPy-basierte numerische Berechnungen für die CityBike-Plattform.

Inhalt:
    - Stations-Distanzmatrix mittels euklidischer Distanz
    - Vektorisierte Fahrtstatistiken (Mittelwert, Median, Perzentile)
    - Ausreißererkennung mittels Z-Scores
    - Vektorisierte Fahrpreisberechnung
"""

import numpy as np
from typing import Dict

# ---------------------------------------------------------------------------
# Distanzberechnungen
# ---------------------------------------------------------------------------



def station_distance_matrix(
    latitudes: np.ndarray, longitudes: np.ndarray
) -> np.ndarray:
    """Berechnet die paarweisen euklidischen Distanzen zwischen Stationen.

    Verwendet ein vereinfachtes ebenes Erdmodell:
        d = sqrt((lat2 - lat1)^2 + (lon2 - lon1)^2)

    Args:
        latitudes: 1-D Array der Stations-Breitengrade.
        longitudes: 1-D Array der Stations-Längengrade.

    Returns:
        Eine 2-D symmetrische Distanzmatrix der Form (n, n).
    """
    # Schritt 1: Berechnung der paarweisen Breitengrad-Differenzen mittels Broadcasting
    lat_diff: np.ndarray = latitudes[:, np.newaxis] - latitudes[np.newaxis, :]

    # Schritt 2: Berechnung der paarweisen Längengrad-Differenzen
    lon_diff: np.ndarray = longitudes[:, np.newaxis] - longitudes[np.newaxis, :]

    # Schritt 3: Kombination mit der euklidischen Formel
    distance_matrix: np.ndarray = np.sqrt(lat_diff**2 + lon_diff**2)
    
    return distance_matrix


# ---------------------------------------------------------------------------
# Fahrtstatistiken
# ---------------------------------------------------------------------------

def trip_duration_stats(durations: np.ndarray) -> Dict[str, float]:
    """Berechnet zusammenfassende Statistiken für die Fahrtdauer.

    Args:
        durations: 1-D Array der Fahrtdauern in Minuten.

    Returns:
        Dict mit den Schlüsseln: mean, median, std, p25, p75, p90.
    """
    stats: Dict[str, float] = {
        "mean": float(np.mean(durations)),
        "median": float(np.median(durations)),
        "std": float(np.std(durations)),
        # Berechnung der Perzentile mittels np.percentile
        "p25": float(np.percentile(durations, 25)),
        "p75": float(np.percentile(durations, 75)),
        "p90": float(np.percentile(durations, 90)),
    }
    return stats


# ---------------------------------------------------------------------------
# Ausreißererkennung
# ---------------------------------------------------------------------------



def detect_outliers_zscore(
    values: np.ndarray, threshold: float = 3.0
) -> np.ndarray:
    """Identifiziert Ausreißer-Indizes mittels der Z-Score-Methode.

    Eine Beobachtung ist ein Ausreißer, wenn |z| > threshold.

    Args:
        values: 1-D Array mit numerischen Werten.
        threshold: Z-Score-Grenzwert (Standard 3.0).

    Returns:
        Boolean-Array — True, wo der Wert ein Ausreißer ist.
    """
    # Schritt 1: Mittelwert und Standardabweichung berechnen
    mean: float = float(np.mean(values))
    std: float = float(np.std(values))

    # Schritt 2: Schutz gegen Division durch Null (wenn std == 0)
    if std == 0:
        return np.zeros_like(values, dtype=bool)

    # Schritt 3: Z-Scores berechnen
    z: np.ndarray = (values - mean) / std

    # Schritt 4: Boolean-Maske zurückgeben
    mask: np.ndarray = np.abs(z) > threshold
    
    return mask


# ---------------------------------------------------------------------------
# Vektorisierte Fahrpreisberechnung
# ---------------------------------------------------------------------------

def calculate_fares(
    durations: np.ndarray,
    distances: np.ndarray,
    per_minute: float,
    per_km: float,
    unlock_fee: float = 0.0,
) -> np.ndarray:
    """Berechnet Fahrpreise für viele Fahrten gleichzeitig mittels NumPy.

    Args:
        durations: 1-D Array der Fahrtdauern (Minuten).
        distances: 1-D Array der Fahrtdistanzen (km).
        per_minute: Kosten pro Minute.
        per_km: Kosten pro km.
        unlock_fee: Pauschale Entsperrgebühr (Standard 0).

    Returns:
        1-D Array der Fahrtpreise.
    """
    # Vektorisierter Ausdruck für alle Fahrten ohne Python-Schleifen
    fares: np.ndarray = unlock_fee + (per_minute * durations) + (per_km * distances)
    
    return fares