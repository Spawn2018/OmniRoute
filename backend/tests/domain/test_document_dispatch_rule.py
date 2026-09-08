import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.document_dispatch_rule import (
    require_dispatch_document_kind,
    require_dispatch_incoterm,
    require_dispatch_source_ref,
    require_dispatch_trade_side,
    require_recipient_role,
)
from app.domain.errors import InvalidDocumentDispatchRule


def test_dispatch_allowlists() -> None:
    assert require_dispatch_incoterm(" dap ") == "DAP"
    assert require_dispatch_trade_side("import") == "import"
    assert require_dispatch_document_kind("commercial_invoice") == "commercial_invoice"
    assert require_recipient_role("omni_customs") == "omni_customs"
    assert require_dispatch_source_ref("tenant:manual") == "tenant:manual"


def test_dispatch_rejects_shipment_document_kind_and_sold_to() -> None:
    with pytest.raises(InvalidDocumentDispatchRule, match="rodzaj"):
        require_dispatch_document_kind("noted")
    with pytest.raises(InvalidDocumentDispatchRule, match="adresata"):
        require_recipient_role("sold_to")
    with pytest.raises(InvalidDocumentDispatchRule, match="obce"):
        require_dispatch_source_ref("mailto:agent@example.com")


@given(st.sampled_from(["noted", "attached", "other"]))
def test_dispatch_kind_is_not_shipment_document_kind(raw: str) -> None:
    with pytest.raises(InvalidDocumentDispatchRule, match="rodzaj"):
        require_dispatch_document_kind(raw)
