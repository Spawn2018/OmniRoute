from datetime import UTC, datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidWeatherObservation
from app.domain.weather_observation import (
    require_condition_code,
    require_observed_at,
    require_provider_code,
    require_station_unlocode,
    require_weather_source_ref,
)


@given(st.sampled_from(["clear", "rain", "snow", "wind", "fog", "ice", "other"]))
def test_condition_code_allowlist(raw: str) -> None:
    assert require_condition_code(raw) == raw


@given(st.sampled_from(["", "storm", "RAIN kg"]))
def test_condition_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidWeatherObservation, match="warunek"):
        require_condition_code(raw)


def test_station_unlocode_uppercases() -> None:
    assert require_station_unlocode(" plgdy ") == "PLGDY"


@given(st.sampled_from(["", "xx", "PL-GDY", "plgd"]))
def test_station_unlocode_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidWeatherObservation, match="stacja"):
        require_station_unlocode(raw)


def test_observed_at_requires_timezone() -> None:
    clock = datetime(2026, 9, 9, 12, 0, tzinfo=UTC)
    assert require_observed_at("2026-09-09T12:00:00+00:00") == clock
    with pytest.raises(InvalidWeatherObservation, match="obserwacja"):
        require_observed_at("")
    with pytest.raises(InvalidWeatherObservation, match="obserwacja"):
        require_observed_at("2026-09-09T12:00:00")


def test_provider_code_is_hitl() -> None:
    assert require_provider_code("hitl") == "hitl"
    with pytest.raises(InvalidWeatherObservation, match="dostawca"):
        require_provider_code("open_meteo")


def test_weather_source_ref_accepts_fixture() -> None:
    assert require_weather_source_ref(" fixture://weather-observation/1 ") == (
        "fixture://weather-observation/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_weather_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidWeatherObservation, match="obce|wskazanie"):
        require_weather_source_ref(raw)
