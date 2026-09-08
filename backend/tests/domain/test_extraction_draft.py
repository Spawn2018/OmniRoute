import pytest

from app.domain.errors import InvalidExtractionDraft
from app.domain.extraction_draft import require_extraction_draft_kind


def test_draft_kind_defaults_to_rate_line() -> None:
    assert require_extraction_draft_kind(None) == "rate_line"


def test_draft_kind_accepts_carrier_quote() -> None:
    assert require_extraction_draft_kind("carrier_quote") == "carrier_quote"


def test_draft_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidExtractionDraft, match="allowlist"):
        require_extraction_draft_kind("purchase_invoice")
