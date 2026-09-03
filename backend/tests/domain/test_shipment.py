from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidShipment
from app.domain.shipment import (
    require_party_on_quotation,
    require_quotation_id,
    require_shipment_source_ref,
    shipment_draft_status,
)


def test_shipment_draft_status_is_draft() -> None:
    assert shipment_draft_status() == "draft"


def test_require_shipment_source_ref_accepts_fixture() -> None:
    assert (
        require_shipment_source_ref(" fixture://shipment/1 ") == "fixture://shipment/1"
    )


def test_require_shipment_source_ref_accepts_manual() -> None:
    assert require_shipment_source_ref("tenant:manual") == "tenant:manual"


@given(st.sampled_from(["", "   ", "http://lists.example/x", "ftp://x"]))
def test_require_shipment_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidShipment):
        require_shipment_source_ref(raw)


def test_require_shipment_source_ref_rejects_too_long() -> None:
    with pytest.raises(InvalidShipment, match="długie"):
        require_shipment_source_ref("fixture://shipment/" + ("a" * 250))


def test_require_quotation_id_rejects_text() -> None:
    with pytest.raises(InvalidShipment, match="UUID"):
        require_quotation_id("quote")  # type: ignore[arg-type]


def test_require_quotation_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_quotation_id(token) == token


def test_require_party_on_quotation_rejects_missing() -> None:
    with pytest.raises(InvalidShipment, match="kontrahenta"):
        require_party_on_quotation(None)


def test_require_party_on_quotation_keeps_uuid() -> None:
    token = uuid4()
    assert require_party_on_quotation(token) == token
