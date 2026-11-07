from pipeline_forge.generator import generate_events
from pipeline_forge.ingestion import split


def test_generate_zero_count_returns_empty() -> None:
    assert generate_events(0) == []


def test_generate_returns_valid_events() -> None:
    generated_events = generate_events(50)
    events, rejections = split(generated_events)

    assert rejections == []
    assert len(events) == 50
