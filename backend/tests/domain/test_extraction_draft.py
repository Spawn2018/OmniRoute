from uuid import uuid4

import pytest

from app.domain.errors import InvalidExtractionDraft, InvalidTenderRfpIntake
from app.domain.extraction_draft import (
    require_extraction_draft_kind,
    require_tender_rfp_payload,
)


def test_draft_kind_defaults_to_rate_line() -> None:
    assert require_extraction_draft_kind(None) == "rate_line"


def test_draft_kind_accepts_carrier_quote() -> None:
    assert require_extraction_draft_kind("carrier_quote") == "carrier_quote"


def test_draft_kind_accepts_tender_rfp() -> None:
    assert require_extraction_draft_kind("tender_rfp") == "tender_rfp"


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
