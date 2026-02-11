"""
Domain-Modelle für die CityBike Bike-Sharing Analytics Plattform.
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ---------------------------------------------------------------------------
# Abstract Base Class
# ---------------------------------------------------------------------------

class Entity(ABC):
    """Abstract base class for all domain entities."""

    def __init__(self, id: str, created_at: datetime | None = None) -> None:
        if not id or not isinstance(id, str):
            raise ValueError("id must be a non-empty string")
        self._id = id
        self._created_at = created_at or datetime.now()

    @property
    def id(self) -> str:
        """Return the entity's unique identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Return the creation timestamp."""
        return self._created_at

    @abstractmethod
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        ...


# ---------------------------------------------------------------------------
# Bike hierarchy
# ---------------------------------------------------------------------------

class Bike(Entity):
    """Represents a bike in the sharing system."""

    VALID_STATUSES = {"available", "in_use", "maintenance"}

    def __init__(
        self,
        bike_id: str,
        bike_type: str,
        status: str = "available",
    ) -> None:
        super().__init__(id=bike_id)
        if bike_type not in ("classic", "electric"):
            raise ValueError(f"Invalid bike_type: {bike_type}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        self._bike_type = bike_type
        self._status = status

    @property
    def bike_type(self) -> str:
        return self._bike_type

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}")
        self._status = value

    def __str__(self) -> str:
        return f"Bike({self.id}, {self.bike_type}, {self.status})"

    def __repr__(self) -> str:
        return (
            f"Bike(bike_id={self.id!r}, bike_type={self.bike_type!r}, "
            f"status={self.status!r})"
        )


class ClassicBike(Bike):
    """A classic (non-electric) bike with gears."""

    def __init__(
        self,
        bike_id: str,
        gear_count: int = 7,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="classic", status=status)
        if gear_count <= 0:
            raise ValueError("gear_count must be positive")
        self._gear_count = gear_count

    @property
    def gear_count(self) -> int:
        return self._gear_count

    def __str__(self) -> str:
        return f"ClassicBike({self.id}, gears={self.gear_count})"

    def __repr__(self) -> str:
        return (
            f"ClassicBike(bike_id={self.id!r}, gear_count={self.gear_count}, "
            f"status={self.status!r})"
        )


class ElectricBike(Bike):
    """An electric bike with a battery."""

    def __init__(
        self,
        bike_id: str,
        battery_level: float = 100.0,
        max_range_km: float = 50.0,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="electric", status=status)
        if not (0 <= battery_level <= 100):
            raise ValueError("battery_level muss zwischen 0 und 100 liegen")
        if max_range_km <= 0:
            raise ValueError("max_range_km muss positiv sein")
        self._battery_level = battery_level
        self._max_range_km = max_range_km

    @property
    def battery_level(self) -> float:
        return self._battery_level

    @property
    def max_range_km(self) -> float:
        return self._max_range_km

    def __str__(self) -> str:
        return f"ElectricBike({self.id}, Akku={self.battery_level}%)"

    def __repr__(self) -> str:
        return (
            f"ElectricBike(bike_id={self.id!r}, battery_level={self.battery_level}, "
            f"status={self.status!r})"
        )


# ---------------------------------------------------------------------------
# Station
# ---------------------------------------------------------------------------

class Station(Entity):
    """Represents a bike-sharing station."""

    def __init__(
        self,
        station_id: str,
        name: str,
        capacity: int,
        latitude: float,
        longitude: float,
    ) -> None:
        super().__init__(id=station_id)
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not (-90 <= latitude <= 90):
            raise ValueError("latitude must be in [-90, 90]")
        if not (-180 <= longitude <= 180):
            raise ValueError("longitude must be in [-180, 180]")
        self._name = name
        self._capacity = capacity
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"Station({self.name})"

    def __repr__(self) -> str:
        return f"Station(station_id={self.id!r}, name={self.name!r})"


# ---------------------------------------------------------------------------
# User hierarchy
# ---------------------------------------------------------------------------

class User(Entity):
    """Base class for a system user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        user_type: str,
    ) -> None:
        super().__init__(id=user_id)
        if "@" not in email:
            raise ValueError("Invalid email format")
        self._name = name
        self._email = email
        self._user_type = user_type

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"User({self.name})"

    def __repr__(self) -> str:
        return f"User(user_id={self.id!r}, name={self.name!r})"


class CasualUser(User):
    """A casual (non-member) user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        day_pass_count: int = 0,
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="casual")
        if day_pass_count < 0:
            raise ValueError("day_pass_count must be >= 0")
        self._day_pass_count = day_pass_count

    def __str__(self) -> str:
        return f"CasualUser({self.name}, passes={self._day_pass_count})"

    def __repr__(self) -> str:
        return f"CasualUser(user_id={self.id!r}, day_pass_count={self._day_pass_count})"


class MemberUser(User):
    """A registered member user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        membership_start: datetime = None,
        membership_end: datetime = None,
        tier: str = "basic",
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="member")
        if tier not in ("basic", "premium"):
            raise ValueError("tier must be 'basic' or 'premium'")
        if membership_start and membership_end and membership_end < membership_start:
            raise ValueError("membership_end must be >= membership_start")
        self._membership_start = membership_start
        self._membership_end = membership_end
        self._tier = tier

    def __str__(self) -> str:
        return f"MemberUser({self.name}, tier={self._tier})"

    def __repr__(self) -> str:
        return f"MemberUser(user_id={self.id!r}, tier={self._tier!r})"


# ---------------------------------------------------------------------------
# Trip
# ---------------------------------------------------------------------------

class Trip:
    """Represents a single bike trip."""

    def __init__(
        self,
        trip_id: str,
        user: User,
        bike: Bike,
        start_station: Station,
        end_station: Station,
        start_time: datetime,
        end_time: datetime,
        distance_km: float,
    ) -> None:
        if distance_km < 0:
            raise ValueError("distance_km must be >= 0")
        if end_time < start_time:
            raise ValueError("end_time must be >= start_time")
        self.trip_id = trip_id
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = distance_km

    @property
    def duration_minutes(self) -> float:
        """Calculate trip duration in minutes from start and end times."""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60

    def __str__(self) -> str:
        return f"Trip({self.trip_id})"

    def __repr__(self) -> str:
        return f"Trip(trip_id={self.trip_id!r})"


# ---------------------------------------------------------------------------
# MaintenanceRecord
# ---------------------------------------------------------------------------

class MaintenanceRecord:
    """Represents a maintenance event for a bike."""

    VALID_TYPES = {
        "tire_repair",
        "brake_adjustment",
        "battery_replacement",
        "chain_lubrication",
        "general_inspection",
    }

    def __init__(
        self,
        record_id: str,
        bike: Bike,
        date: datetime,
        maintenance_type: str,
        cost: float,
        description: str = "",
    ) -> None:
        if maintenance_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid maintenance type: {maintenance_type}")
        if cost < 0:
            raise ValueError("cost must be >= 0")
        self.record_id = record_id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = cost
        self.description = description

    def __str__(self) -> str:
        return f"MaintenanceRecord({self.record_id}, {self.maintenance_type})"

    def __repr__(self) -> str:
        return f"MaintenanceRecord(record_id={self.record_id!r})"
