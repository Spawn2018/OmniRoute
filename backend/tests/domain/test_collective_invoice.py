from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.collective_invoice import (
    require_collective_extra_shipment,
    require_collective_invoice_id,
    require_collective_same_party,
    require_collective_shipment_id,
    require_collective_source_ref,
)
from app.domain.errors import InvalidCollectiveInvoice


def test_require_collective_source_ref_accepts_fixture() -> None:
    assert (
        require_collective_source_ref(" fixture://collective-invoice/1 ")
        == "fixture://collective-invoice/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_collective_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCollectiveInvoice):
        require_collective_source_ref(raw)


def test_require_collective_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_collective_invoice_id(token) == token
    assert require_collective_shipment_id(token) == token


def test_require_collective_ids_reject_text() -> None:
    with pytest.raises(InvalidCollectiveInvoice, match="UUID"):
        require_collective_invoice_id("c")  # type: ignore[arg-type]
    with pytest.raises(InvalidCollectiveInvoice, match="UUID"):
        require_collective_shipment_id("s")  # type: ignore[arg-type]


def test_require_collective_extra_rejects_anchor() -> None:
    token = uuid4()
    with pytest.raises(InvalidCollectiveInvoice, match="kotwicą"):
        require_collective_extra_shipment(token, token)


def test_require_collective_same_party_rejects_foreign_customer() -> None:
    with pytest.raises(InvalidCollectiveInvoice, match="kontrahenta"):
        require_collective_same_party(uuid4(), uuid4())
