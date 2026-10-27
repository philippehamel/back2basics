import json
from pathlib import Path


def ingest_events(path: Path) -> list[object]:
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise TypeError(f"expected list, got {type(data).__name__} from {path}")
    return data
