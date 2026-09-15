from uuid import uuid4

import pytest

from app.domain.errors import (
    ExtractionCandidatesNotEditable,
    InvalidExtractionDraft,
    InvalidTenderRfpIntake,
)
from app.domain.extraction_draft import (
    next_extraction_revision,
    require_extract_path,
    require_extraction_draft_kind,
    require_rate_candidates_editable,
    require_tender_rfp_payload,
)


def test_draft_kind_defaults_to_rate_line() -> None:
    assert require_extraction_draft_kind(None) == "rate_line"


def test_draft_kind_accepts_carrier_quote() -> None:
    assert require_extraction_draft_kind("carrier_quote") == "carrier_quote"


def test_draft_kind_accepts_tender_rfp() -> None:
    assert require_extraction_draft_kind("tender_rfp") == "tender_rfp"


def test_extract_path_defaults_to_text() -> None:
    assert require_extract_path(None) == "text"
    assert require_extract_path("image") == "image"
    with pytest.raises(InvalidExtractionDraft, match="allowlist"):
        require_extract_path("pixels")
    with pytest.raises(InvalidExtractionDraft, match="tekstem"):
        require_extract_path(1)


def test_next_extraction_revision_bumps_or_starts() -> None:
    assert next_extraction_revision(0) == 1
    assert next_extraction_revision(3) == 4
    assert next_extraction_revision(None) == 1
    assert next_extraction_revision(True) == 1


def test_rate_candidates_editable_allowlist() -> None:
    require_rate_candidates_editable("rate_line")
    require_rate_candidates_editable("carrier_quote")
    require_rate_candidates_editable("tender_rfp")
    with pytest.raises(ExtractionCandidatesNotEditable, match="rate_line"):
        require_rate_candidates_editable("purchase_invoice")


def test_draft_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidExtractionDraft, match="allowlist"):
        require_extraction_draft_kind("purchase_invoice")


def test_tender_rfp_payload_reads_board_and_code() -> None:
    board = uuid4()
    stored = require_tender_rfp_payload({"tender_id": str(board), "intake_code": "scope"})
    assert stored.tender_id == board
    assert stored.intake_code == "scope"


def test_tender_rfp_payload_rejects_empty_code() -> None:
    with pytest.raises(InvalidTenderRfpIntake, match="przyjęcie"):
        require_tender_rfp_payload({"tender_id": str(uuid4()), "intake_code": "X"})
