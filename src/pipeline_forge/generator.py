from datetime import UTC, datetime, timedelta
from enum import Enum
from random import choice, randint, uniform


def generate_random_timestamp(start_year: int = 2025, end_year: int = 2026) -> str:
    start_date = datetime(start_year, 1, 1, tzinfo=UTC)
    end_date = datetime(end_year, 12, 31, 23, 59, 59, tzinfo=UTC)
    time_delta = end_date - start_date

    total_seconds = int(time_delta.total_seconds())
    random_seconds = randint(0, total_seconds)
    random_date = start_date + timedelta(seconds=random_seconds)

    return random_date.strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_events(count: int) -> list[dict[str, object]]:
    returned_events = []

    Device_id = Enum("Device_id", "cam_001 cam_002 cam_003")
    Event_type = Enum("Event_type", "temperature inference upload")

    for _ in range(count):
        random_device = choice(list(Device_id))
        random_event = choice(list(Event_type))

        device_str = random_device.name.replace("_", "-")
        event_str = random_event.name

        random_value = round(uniform(10.0, 100.0), 2)

        event_data = {
            "device_id": device_str,
            "timestamp": generate_random_timestamp(),
            "event_type": event_str,
            "value": random_value,
        }

        returned_events.append(event_data)

    return returned_events
