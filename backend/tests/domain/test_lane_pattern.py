import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidLanePattern
from app.domain.lane_pattern import require_pattern_pair, require_pattern_source_ref


def test_pattern_pair_normalizes_unlocode() -> None:
    origin, dest = require_pattern_pair(" plgdy ", "deham")
    assert origin == "PLGDY"
    assert dest == "DEHAM"
    assert require_pattern_source_ref(" fixture://lane-pattern/1 ") == (
        "fixture://lane-pattern/1"
    )


def test_pattern_rejects_empty_and_foreign_ref() -> None:
    with pytest.raises(InvalidLanePattern, match="wzorzec"):
        require_pattern_pair("  ", "DEHAM")
    with pytest.raises(InvalidLanePattern, match="wzorzec"):
        require_pattern_pair("PLGDY", "PLGDY")
    with pytest.raises(InvalidLanePattern, match="obce"):
        require_pattern_source_ref("https://evil.example/pattern")


_UNLOCODE = st.from_regex(r"[A-Z]{2}[A-Z0-9]{3}", fullmatch=True)


@given(_UNLOCODE)
def test_identical_ends_are_always_wzorzec(code: str) -> None:
    with pytest.raises(InvalidLanePattern, match="wzorzec"):
        require_pattern_pair(code, code)
