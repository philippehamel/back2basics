import json
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from pipeline_forge.models import Event, Rejection


def ingest_events(path: Path) -> list[object]:
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise TypeError(f"expected list, got {type(data).__name__} from {path}")
    return data


def validate(item: object) -> Event | Rejection:
    if not isinstance(item, dict):
        return Rejection(
            raw=item, errors=(f"expected dict, got {type(item).__name__}",)
        )
    error_list: list[str] = []

    if "device_id" not in item:
        error_list.append("device_id: missing")
    elif not isinstance(item["device_id"], str):
        error_list.append(
            f"device_id: expected str, got {type(item['device_id']).__name__}"
        )

    parsed_timestamp: datetime | None = None

    if "timestamp" not in item:
        error_list.append("timestamp: missing")
    elif not isinstance(item["timestamp"], str):
        error_list.append(
            f"timestamp: expected str, got {type(item['timestamp']).__name__}"
        )
    else:
        try:
            parsed_timestamp = datetime.fromisoformat(item["timestamp"])
        except ValueError:
            error_list.append("timestamp: not ISO 8601")
        else:
            if parsed_timestamp.tzinfo is None:
                error_list.append("timestamp: missing tz")

    if "event_type" not in item:
        error_list.append("event_type: missing")
    elif not isinstance(item["event_type"], str):
        error_list.append(
            f"event_type: expected str, got {type(item['event_type']).__name__}"
        )
    elif item["event_type"] == "":
        error_list.append("event_type: is empty")

    if "value" not in item:
        error_list.append("value: missing")
    elif isinstance(item["value"], bool) or not isinstance(item["value"], (int, float)):
        error_list.append(f"value: expected float, got {type(item['value']).__name__}")

    if error_list or parsed_timestamp is None:
        return Rejection(item, errors=tuple(error_list))
    else:
        return Event(
            device_id=item["device_id"],
            timestamp=parsed_timestamp,
            event_type=item["event_type"],
            value=float(item["value"]),
        )


def split(items: Sequence[object]) -> tuple[list[Event], list[Rejection]]:
    events: list[Event] = []
    rejections: list[Rejection] = []
    for item in items:
        result = validate(item)
        if isinstance(result, Event):
            events.append(result)
        else:
            rejections.append(result)
    return (events, rejections)
