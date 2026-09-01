"""Wejście ingestu w testach — plik na dysku, nigdy sieć."""

from pathlib import Path

from app.services.geography.unlocode_ingest import UnlocodeRecord, parse_unlocode_records

FIXTURE_SOURCE_REF = "github:cristan/improved-un-locodes@fixture"

_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "unlocode_sample.json"


def sample_records() -> list[UnlocodeRecord]:
    return parse_unlocode_records(_FIXTURE.read_text(encoding="utf-8"))
