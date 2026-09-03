from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidSalesInvoice
from app.domain.sales_invoice import (
    require_invoice_kind,
    require_invoice_ref,
    require_invoice_shipment_id,
    require_invoice_source_ref,
    require_ksef_ref,
)


def test_require_invoice_kind_accepts_allowlist() -> None:
    assert require_invoice_kind(" issued ") == "issued"
    assert require_invoice_kind("noted") == "noted"
    assert require_invoice_kind("other") == "other"


def test_require_invoice_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidSalesInvoice, match="rodzaj"):
        require_invoice_kind("hold")


def test_require_invoice_ref_trims() -> None:
    assert require_invoice_ref(" FV/2026/1 ") == "FV/2026/1"


@given(st.sampled_from(["", "   "]))
def test_require_invoice_ref_rejects_blank(raw: str) -> None:
    with pytest.raises(InvalidSalesInvoice, match="numer"):
        require_invoice_ref(raw)


def test_require_invoice_source_ref_accepts_fixture() -> None:
    assert (
        require_invoice_source_ref(" fixture://sales-invoice/1 ")
        == "fixture://sales-invoice/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_invoice_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidSalesInvoice):
        require_invoice_source_ref(raw)


def test_require_invoice_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidSalesInvoice, match="UUID"):
        require_invoice_shipment_id("inv")  # type: ignore[arg-type]


def test_require_invoice_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_invoice_shipment_id(token) == token


def test_require_ksef_ref_accepts_allowlist() -> None:
    assert require_ksef_ref(" fixture://ksef/1 ") == "fixture://ksef/1"
    assert require_ksef_ref("ksef://sesja") == "ksef://sesja"


@given(st.sampled_from(["", "   ", "https://example.test/ksef"]))
def test_require_ksef_ref_rejects_blank_and_http(raw: str) -> None:
    with pytest.raises(InvalidSalesInvoice, match="sesji"):
        require_ksef_ref(raw)
