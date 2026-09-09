import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidFreeTimeClock
from app.domain.free_time_clock import (
    require_clock_kind,
    require_clock_source_ref,
    require_free_days,
)


@given(st.sampled_from(["demurrage", "detention", "mixed", "rollover"]))
def test_clock_kind_allowlist(raw: str) -> None:
    assert require_clock_kind(raw) == raw


@given(st.sampled_from(["", "eta", "DEMURRAGE kg"]))
def test_clock_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidFreeTimeClock, match="rodzaj"):
        require_clock_kind(raw)


@given(st.integers(min_value=0, max_value=3650))
def test_free_days_accepts_non_negative(raw: int) -> None:
    assert require_free_days(raw) == raw


def test_free_days_rejects_negative_and_bool() -> None:
    with pytest.raises(InvalidFreeTimeClock, match="dni"):
        require_free_days(-1)
    with pytest.raises(InvalidFreeTimeClock, match="dni"):
        require_free_days(True)


def test_clock_source_ref_accepts_fixture() -> None:
    assert (
        require_clock_source_ref(" fixture://free-time-clock/1 ") == "fixture://free-time-clock/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_clock_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidFreeTimeClock, match="obce|wskazanie"):
        require_clock_source_ref(raw)
