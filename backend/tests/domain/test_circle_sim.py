import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.circle_sim import (
    require_circle_pair,
    require_circle_source_ref,
    require_sim_code,
)
from app.domain.errors import InvalidCircleSim


@given(st.sampled_from(["backhaul_a", "kolko_1", "ab"]))
def test_sim_code_accepts_snake(raw: str) -> None:
    assert require_sim_code(f" {raw} ") == raw


@given(st.sampled_from(["", "X", "1bad", "KOLKO", "circle-sim"]))
def test_sim_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidCircleSim, match="kolko"):
        require_sim_code(raw)


def test_circle_pair_normalizes_unlocode() -> None:
    unload, load = require_circle_pair(" plgdy ", "deham")
    assert unload == "PLGDY"
    assert load == "DEHAM"
    assert require_circle_source_ref(" fixture://circle-sim/1 ") == (
        "fixture://circle-sim/1"
    )
    assert require_circle_source_ref("tenant:manual") == "tenant:manual"


def test_circle_rejects_bad_ends_and_foreign_ref() -> None:
    with pytest.raises(InvalidCircleSim, match="rozladunek"):
        require_circle_pair("  ", "DEHAM")
    with pytest.raises(InvalidCircleSim, match="zaladunek"):
        require_circle_pair("PLGDY", "xx")
    with pytest.raises(InvalidCircleSim, match="para"):
        require_circle_pair("PLGDY", "PLGDY")
    with pytest.raises(InvalidCircleSim, match="obce"):
        require_circle_source_ref("https://evil.example/circle")


_UNLOCODE = st.from_regex(r"[A-Z]{2}[A-Z0-9]{3}", fullmatch=True)


@given(_UNLOCODE)
def test_identical_ends_are_always_para(code: str) -> None:
    with pytest.raises(InvalidCircleSim, match="para"):
        require_circle_pair(code, code)
