from datetime import date

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.charge_template import (
    require_member_code,
    require_template_code,
    require_template_source_ref,
    require_validity_window,
)
from app.domain.errors import InvalidChargeTemplate


@given(st.sampled_from(["spot_thc", "ltl_west", "weekend"]))
def test_template_code_normalizes_snake(raw: str) -> None:
    assert require_template_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_template_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidChargeTemplate, match="szablon"):
        require_template_code(raw)


@given(st.sampled_from(["THC", "thc", "BAF"]))
def test_member_code_normalizes_catalog_token(raw: str) -> None:
    assert require_member_code(raw) == raw.strip().upper()


@given(st.sampled_from(["", "x", "thc!", "a" * 33]))
def test_member_code_rejects_non_catalog_token(raw: str) -> None:
    with pytest.raises(InvalidChargeTemplate, match="kod"):
        require_member_code(raw)


def test_validity_window_keeps_ordered_iso_dates() -> None:
    start, end = require_validity_window("2026-01-01", "2026-12-31")
    assert start == date(2026, 1, 1)
    assert end == date(2026, 12, 31)


@given(st.sampled_from([("", "2026-01-01"), ("2026-12-31", "2026-01-01"), ("nope", "2026-01-01")]))
def test_validity_window_rejects_empty_inverted_and_garbage(pair: tuple[str, str]) -> None:
    with pytest.raises(InvalidChargeTemplate, match="ważność"):
        require_validity_window(pair[0], pair[1])


def test_template_source_ref_accepts_fixture() -> None:
    assert (
        require_template_source_ref(" fixture://charge-template/1 ")
        == "fixture://charge-template/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_template_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidChargeTemplate):
        require_template_source_ref(raw)
