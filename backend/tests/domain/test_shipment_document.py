from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidShipmentDocument
from app.domain.shipment_document import (
    require_document_kind,
    require_document_shipment_id,
    require_document_source_ref,
)


def test_require_document_kind_accepts_allowlist() -> None:
    assert require_document_kind(" noted ") == "noted"
    assert require_document_kind("attached") == "attached"
    assert require_document_kind("other") == "other"


def test_require_document_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidShipmentDocument, match="rodzaj"):
        require_document_kind("hbl")


def test_require_document_source_ref_accepts_fixture() -> None:
    assert (
        require_document_source_ref(" fixture://shipment-document/1 ")
        == "fixture://shipment-document/1"
    )


@given(st.sampled_from(["", "   ", "http://files.example/x"]))
def test_require_document_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidShipmentDocument):
        require_document_source_ref(raw)


def test_require_document_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidShipmentDocument, match="UUID"):
        require_document_shipment_id("doc")  # type: ignore[arg-type]


def test_require_document_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_document_shipment_id(token) == token
