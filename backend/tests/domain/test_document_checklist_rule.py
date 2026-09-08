import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.document_checklist_rule import (
    require_blocks_dispatch,
    require_checklist_document_kind,
    require_checklist_incoterm,
    require_checklist_mode,
    require_checklist_trade_side,
)
from app.domain.errors import InvalidDocumentChecklistRule


def test_checklist_allowlists() -> None:
    assert require_checklist_incoterm(" fob ") == "FOB"
    assert require_checklist_trade_side("export") == "export"
    assert require_checklist_mode("ocean") == "ocean"
    assert require_checklist_document_kind("bill_of_lading") == "bill_of_lading"
    assert require_blocks_dispatch(True) is True


def test_checklist_rejects_unknown_kind() -> None:
    with pytest.raises(InvalidDocumentChecklistRule, match="rodzaj"):
        require_checklist_document_kind("noted")


def test_checklist_rejects_non_bool_flag() -> None:
    with pytest.raises(InvalidDocumentChecklistRule, match="flagą"):
        require_blocks_dispatch("true")  # type: ignore[arg-type]


@given(st.sampled_from(["noted", "attached", "other", "invoice"]))
def test_checklist_kind_is_not_shipment_document_kind(raw: str) -> None:
    with pytest.raises(InvalidDocumentChecklistRule, match="rodzaj"):
        require_checklist_document_kind(raw)
