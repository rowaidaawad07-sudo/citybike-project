"""
Factory Pattern — Erstellung von Domänenobjekten aus CSV-Daten (Dictionaries).
Die Factory-Funktionen verbergen, welche konkrete Unterklasse instanziiert wird.
"""

from typing import Dict, Any
from datetime import datetime
from models import (
    Bike,
    ClassicBike,
    ElectricBike,
    User,
    CasualUser,
    MemberUser,
    Station,
    Trip,
    MaintenanceRecord
)


def create_bike(data: Dict[str, Any]) -> Bike:
    """Erstellt ein Bike (ClassicBike oder ElectricBike) aus einem Daten-Dictionary."""
    bike_type = str(data.get("bike_type", "")).lower()

    if bike_type == "classic":
        return ClassicBike(
            bike_id=data["bike_id"],
            gear_count=int(data.get("gear_count", 7)),
        )
    elif bike_type == "electric":
        return ElectricBike(
            bike_id=data["bike_id"],
            battery_level=float(data.get("battery_level", 100.0)),
            max_range_km=float(data.get("max_range_km", 60.0)),
        )
    else:
        raise ValueError(f"Unbekannter bike_type: {bike_type!r}")


def create_user(data: Dict[str, Any]) -> User:
    """Erstellt einen User (CasualUser or MemberUser) aus einem Daten-Dictionary."""
    user_type = str(data.get("user_type", "")).lower()

    if user_type == "member":
        return MemberUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data.get("email", ""),
            membership_start=datetime.strptime(data.get("membership_start", "2024-01-01"), "%Y-%m-%d") if data.get("membership_start") else None,
            membership_end=datetime.strptime(data.get("membership_end", "2024-12-31"), "%Y-%m-%d") if data.get("membership_end") else None,
            tier=data.get("tier", "basic")
        )
    elif user_type == "casual":
        return CasualUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data.get("email", ""),
            day_pass_count=int(data.get("day_pass_count", 0))
        )
    else:
        raise ValueError(f"Unbekannter user_type: {user_type!r}")


def create_station(data: Dict[str, Any]) -> Station:
    """Erstellt ein Station-Objekt aus einem Dictionary."""
    return Station(
        station_id=data["station_id"],
        name=data["station_name"],
        capacity=int(data.get("capacity", 20)),
        latitude=float(data.get("latitude", 0.0)),
        longitude=float(data.get("longitude", 0.0))
    )


def create_trip(data: Dict[str, Any], user: User, bike: Bike, start_station: Station, end_station: Station) -> Trip:
    """Erstellt ein Trip-Objekt aus einem Dictionary und den zugehörigen Objekten."""
    return Trip(
        trip_id=data["trip_id"],
        user=user,
        bike=bike,
        start_station=start_station,
        end_station=end_station,
        start_time=datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S"),
        end_time=datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S"),
        distance_km=float(data["distance_km"])
    )


def create_maintenance_record(data: Dict[str, Any], bike: Bike) -> MaintenanceRecord:
    """Erstellt ein MaintenanceRecord-Objekt aus einem Dictionary und einem Bike-Objekt."""
    return MaintenanceRecord(
        record_id=data["record_id"],
        bike=bike,
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        maintenance_type=data["maintenance_type"],
        cost=float(data["cost"]),
        description=data.get("description", "")
    )