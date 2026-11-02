import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from pipeline_forge.ingestion import ingest_events, split, validate
from pipeline_forge.models import Event, Rejection


def test_validate_rejects_non_dict() -> None:
    assert validate("42") == Rejection(raw="42", errors=("expected dict, got str",))


def test_validate_accepts_valid_record() -> None:
    item: object = {
        "device_id": "cam-001",
        "timestamp": "1999-12-31T23:59:00Z",
        "event_type": "inference",
        "value": 42,
    }
    assert validate(item) == Event(
        device_id="cam-001",
        timestamp=datetime(1999, 12, 31, 23, 59, tzinfo=UTC),
        event_type="inference",
        value=42.0,
    )


def test_validate_rejects_missing_fields() -> None:
    item = {
        "device_id": "cam-001",
        "timestamp": "1999-12-31T23:59:00Z",
        "value": 42,
    }
    assert validate(item) == Rejection(item, ("event_type: missing",))


def test_validate_rejects_wrong_type() -> None:
    item = {
        "device_id": "cam-001",
        "timestamp": "1999-12-31T23:59:00Z",
        "event_type": "inference",
        "value": True,
    }
    assert validate(item) == Rejection(item, ("value: expected float, got bool",))


def test_validate_rejects_bad_iso() -> None:
    item = {
        "device_id": "cam-001",
        "timestamp": "1999-12-32T23:59:00Z",
        "event_type": "inference",
        "value": 42,
    }
    assert validate(item) == Rejection(item, ("timestamp: not ISO 8601",))


def test_validate_rejects_no_tz() -> None:
    item = {
        "device_id": "cam-001",
        "timestamp": "1999-12-31T23:59:00",
        "event_type": "inference",
        "value": 42,
    }
    assert validate(item) == Rejection(item, ("timestamp: missing tz",))


def test_validate_multiple_rejects() -> None:
    item = {
        "device_id": "cam-001",
        "timestamp": "1999-12-31T23:59:00",
        "event_type": "inference",
        "value": True,
    }
    assert validate(item) == Rejection(
        item,
        (
            "timestamp: missing tz",
            "value: expected float, got bool",
        ),
    )


def test_ingest_events_rejects_non_list(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.json"
    file_path.write_text("42")
    with pytest.raises(TypeError):
        ingest_events(file_path)


def test_ingest_events_accepts_valid_path(tmp_path: Path) -> None:
    items = [
        {
            "device_id": "cam-001",
            "timestamp": "1999-12-31T23:59:00",
            "event_type": "inference",
            "value": "42",
        },
        {
            "device_id": "cam-002",
            "timestamp": "1999-12-31T23:59:00",
            "event_type": "inference",
            "value": "22",
        },
    ]
    file_path = tmp_path / "sample.json"
    file_path.write_text(json.dumps(items))
    assert ingest_events(file_path) == items


def test_split_separate_events_and_rejections() -> None:
    items: list[object] = [
        {
            "device_id": "cam-002",
            "timestamp": "1999-12-31T23:59:00Z",
            "event_type": "inference",
            "value": 42,
        },
        {
            "device_id": "cam-001",
            "timestamp": "1999-12-32T23:59:00Z",
            "event_type": "sale",
            "value": 23,
        },
    ]
    events, rejections = split(items)
    assert len(events) == 1
    assert len(rejections) == 1
    assert rejections[0] == Rejection(
        items[1],
        ("timestamp: not ISO 8601",),
    )
    assert events[0] == Event(
        device_id="cam-002",
        timestamp=datetime(1999, 12, 31, 23, 59, tzinfo=UTC),
        event_type="inference",
        value=42.0,
    )
