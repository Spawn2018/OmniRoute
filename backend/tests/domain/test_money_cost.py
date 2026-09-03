from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidMoneyCost
from app.domain.money_cost import (
    require_cost_payment_id,
    require_cost_rate_id,
    require_cost_source_ref,
)


def test_require_cost_source_ref_accepts_fixture() -> None:
    assert require_cost_source_ref(" fixture://money-cost/1 ") == "fixture://money-cost/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_cost_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidMoneyCost):
        require_cost_source_ref(raw)


def test_require_cost_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_cost_payment_id(token) == token
    assert require_cost_rate_id(token) == token


def test_require_cost_ids_reject_text() -> None:
    with pytest.raises(InvalidMoneyCost, match="UUID"):
        require_cost_payment_id("p")  # type: ignore[arg-type]
    with pytest.raises(InvalidMoneyCost, match="UUID"):
        require_cost_rate_id("r")  # type: ignore[arg-type]
