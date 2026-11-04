import json
from datetime import UTC, datetime
from pathlib import Path

from pipeline_forge.load import write_events
from pipeline_forge.models import Event


def test_write_events_multiple_events(tmp_path: Path) -> None:
    file_path: Path = tmp_path / "Events.jsonl"
    events: list[Event] = [
        Event(
            device_id="cam-001",
            timestamp=datetime(1999, 12, 31, 23, 59, tzinfo=UTC),
            event_type="sale",
            value=42,
        ),
        Event(
            device_id="cam-002",
            timestamp=datetime(2999, 12, 31, 23, 59, tzinfo=UTC),
            event_type="sale",
            value=7,
        ),
    ]
    write_events(events, file_path)
    file_content = file_path.read_text().splitlines()
    assert len(file_content) == 2
    assert json.loads(file_content[0])["timestamp"] == "1999-12-31T23:59:00+00:00"
    assert json.loads(file_content[1])["timestamp"] == "2999-12-31T23:59:00+00:00"


def test_write_events_empty_list(tmp_path: Path) -> None:
    file_path: Path = tmp_path / "Events.jsonl"
    write_events([], file_path)
    assert file_path.read_text() == ""


def test_write_events_overwrites_existing_file(tmp_path: Path) -> None:
    file_path: Path = tmp_path / "Events.jsonl"
    events: list[Event] = [
        Event(
            device_id="cam-001",
            timestamp=datetime(1999, 12, 31, 23, 59, tzinfo=UTC),
            event_type="sale",
            value=42,
        ),
        Event(
            device_id="cam-002",
            timestamp=datetime(2999, 12, 31, 23, 59, tzinfo=UTC),
            event_type="sale",
            value=7,
        ),
    ]
    new_events: list[Event] = [
        Event(
            device_id="cam-003",
            timestamp=datetime(6999, 12, 31, 23, 59, tzinfo=UTC),
            event_type="test",
            value=56,
        ),
    ]
    write_events(events, file_path)
    write_events(new_events, file_path)
    file_content = file_path.read_text().splitlines()
    assert len(file_content) == 1
    assert json.loads(file_content[0])["device_id"] == "cam-003"
