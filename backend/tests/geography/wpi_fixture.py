"""Wejście ingestu WPI w testach — plik na dysku, nigdy sieć."""

from pathlib import Path

FIXTURE_SOURCE_REF = "nga:pub150@fixture"

_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "wpi_sample.csv"


def sample_csv() -> str:
    return _FIXTURE.read_text(encoding="utf-8")
