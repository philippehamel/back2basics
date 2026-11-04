import json
from dataclasses import asdict
from pathlib import Path

from pipeline_forge.models import Event


def write_events(events: list[Event], path: Path) -> None:
    with path.open("w") as f:
        for event in events:
            dict_event = asdict(event)
            dict_event["timestamp"] = dict_event["timestamp"].isoformat()
            f.write(json.dumps(dict_event) + "\n")
