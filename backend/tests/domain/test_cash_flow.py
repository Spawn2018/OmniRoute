from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.cash_flow import (
    require_cash_flow_payment_id,
    require_cash_flow_quotation_id,
    require_cash_flow_source_ref,
)
from app.domain.errors import InvalidCashFlow


def test_require_cash_flow_source_ref_accepts_fixture() -> None:
    assert require_cash_flow_source_ref(" fixture://cash-flow/1 ") == "fixture://cash-flow/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_cash_flow_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCashFlow):
        require_cash_flow_source_ref(raw)


def test_require_cash_flow_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_cash_flow_quotation_id(token) == token
    assert require_cash_flow_payment_id(token) == token


def test_require_cash_flow_ids_reject_text() -> None:
    with pytest.raises(InvalidCashFlow, match="UUID"):
        require_cash_flow_quotation_id("q")  # type: ignore[arg-type]
    with pytest.raises(InvalidCashFlow, match="UUID"):
        require_cash_flow_payment_id("p")  # type: ignore[arg-type]
