from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.cash_discount import (
    require_cash_discount_source_ref,
    require_discount_kind,
    require_invoice_id,
)
from app.domain.errors import InvalidCashDiscount


@given(st.sampled_from(["skonto", "reserve", "internal_settlement"]))
def test_discount_kind_normalizes_snake(raw: str) -> None:
    assert require_discount_kind(raw) == raw


@given(st.sampled_from(["", "X", "2%", "http://hold.example/x"]))
def test_discount_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidCashDiscount, match="skonto"):
        require_discount_kind(raw)


def test_cash_discount_source_ref_accepts_fixture() -> None:
    assert require_cash_discount_source_ref(" fixture://cash-discount/1 ") == (
        "fixture://cash-discount/1"
    )
    assert require_invoice_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_cash_discount_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCashDiscount, match="obce|wskazanie"):
        require_cash_discount_source_ref(raw)
