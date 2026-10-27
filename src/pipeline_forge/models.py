from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Event:
    device_id: str
    timestamp: datetime
    event_type: str
    value: float


@dataclass(frozen=True, slots=True)
class Rejection:
    raw: object
    errors: tuple[str, ...]
