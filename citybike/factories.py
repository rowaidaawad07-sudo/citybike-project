"""
Factory Pattern — Erstellung von Domänenobjekten aus CSV-Daten (Dictionaries).

Die Factory-Funktionen verbergen, welche konkrete Unterklasse instanziiert wird,
sodass der Rest des Codes ClassicBike / ElectricBike etc. nicht direkt importieren muss.
"""

from citybike.models import (
    Bike,
    ClassicBike,
    ElectricBike,
    User,
    CasualUser,
    MemberUser,
)


def create_bike(data: dict) -> Bike:
    """
    Erstellt ein Bike (ClassicBike oder ElectricBike) aus einem Daten-Dictionary.

    Args:
        data: Ein Dict mit mindestens 'bike_id' und 'bike_type'.

    Returns:
        Eine Instanz von ClassicBike oder ElectricBike.

    Raises:
        ValueError: Wenn der bike_type unbekannt ist.
    """
    bike_type = data.get("bike_type", "").lower()

    if bike_type == "classic":
        return ClassicBike(
            bike_id=data["bike_id"],
            gear_count=int(data.get("gear_count", 7)),
        )
    elif bike_type == "electric":
        return ElectricBike(
            bike_id=data["bike_id"],
            battery_level=float(data.get("battery_level", 100.0)),
            max_range_km=float(data.get("max_range_km", 50.0)),
        )
    else:
       raise ValueError(f"Unknown bike_type: {bike_type}")


def create_user(data: dict) -> User:
    """
    Erstellt einen User (CasualUser oder MemberUser) aus einem Daten-Dictionary.

    Args:
        data: Ein Dict mit mindestens 'user_id', 'name', 'email', 'user_type'.

    Returns:
        Eine Instanz von CasualUser oder MemberUser.
        
    Raises:
        ValueError: Wenn der user_type unbekannt ist.
        
    Example:
        >>> user = create_user({"user_id": "U101", "user_type": "member", "name": "Max", "email": "max@mail.com"})
        >>> isinstance(user, MemberUser)
        True
    """
    # Bestimmung des Benutzertyps aus den Daten
    user_type = data.get("user_type", "").lower()

    if user_type == "casual":
        return CasualUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"]
        )
    elif user_type == "member":
        return MemberUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            membership_id=data.get("membership_id", "N/A")
        )
    else:
        # Fehlermeldung, wenn der Typ nicht zugeordnet werden kann
        raise ValueError(f"Unbekannter user_type: {user_type!r}")