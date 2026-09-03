from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidFxDifference
from app.domain.fx_difference import (
    require_fx_quotation_id,
    require_fx_rate_id,
    require_fx_source_ref,
)


def test_require_fx_source_ref_accepts_fixture() -> None:
    assert require_fx_source_ref(" fixture://fx-difference/1 ") == "fixture://fx-difference/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_fx_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidFxDifference):
        require_fx_source_ref(raw)


def test_require_fx_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_fx_quotation_id(token) == token
    assert require_fx_rate_id(token) == token


def test_require_fx_ids_reject_text() -> None:
    with pytest.raises(InvalidFxDifference, match="UUID"):
        require_fx_quotation_id("q")  # type: ignore[arg-type]
    with pytest.raises(InvalidFxDifference, match="UUID"):
        require_fx_rate_id("r")  # type: ignore[arg-type]
