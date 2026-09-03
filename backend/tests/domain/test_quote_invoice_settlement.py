from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidQuoteInvoiceSettlement
from app.domain.quote_invoice_settlement import (
    require_settlement_invoice_id,
    require_settlement_quotation_id,
    require_settlement_source_ref,
)


def test_require_settlement_source_ref_accepts_fixture() -> None:
    assert (
        require_settlement_source_ref(" fixture://quote-invoice-settlement/1 ")
        == "fixture://quote-invoice-settlement/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_settlement_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidQuoteInvoiceSettlement):
        require_settlement_source_ref(raw)


def test_require_settlement_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_settlement_quotation_id(token) == token
    assert require_settlement_invoice_id(token) == token


def test_require_settlement_ids_reject_text() -> None:
    with pytest.raises(InvalidQuoteInvoiceSettlement, match="UUID"):
        require_settlement_quotation_id("q")  # type: ignore[arg-type]
    with pytest.raises(InvalidQuoteInvoiceSettlement, match="UUID"):
        require_settlement_invoice_id("i")  # type: ignore[arg-type]
