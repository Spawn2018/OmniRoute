import json
from pathlib import Path

import pytest

from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.domain.errors import InvalidExtractionDraft
from app.domain.extraction_draft import unmatched_golden_candidates

_OWNED = Path(__file__).resolve().parent / "golden" / "owned.json"
_DOMAIN = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "domain"
    / "extraction_draft.py"
)


def _owned_cases() -> list[object]:
    raw = json.loads(_OWNED.read_text(encoding="utf-8"))
    assert type(raw) is list
    assert len(raw) >= 500
    return raw


def test_owned_golden_matches_mock_extractor() -> None:
    extractor = MockExtractor()
    for case in _owned_cases():
        assert type(case) is dict
        source_ref = case["source_ref"]
        input_text = case["input_text"]
        expected = case["expected"]
        assert type(source_ref) is str
        assert type(input_text) is str
        payload = extractor.extract(source_ref=source_ref, input_text=input_text)
        dumped = [row.model_dump() for row in payload.candidates]
        assert unmatched_golden_candidates(dumped, expected) == []


def test_unmatched_golden_reports_missing_code() -> None:
    missing = unmatched_golden_candidates(
        [{"code": "THC", "amount_text": "100", "currency": "EUR"}],
        [{"code": "BAF", "amount_text": "12", "currency": "USD"}],
    )
    assert missing == [("BAF", "12", "USD")]


def test_unmatched_golden_rejects_non_list() -> None:
    with pytest.raises(InvalidExtractionDraft, match="listy"):
        unmatched_golden_candidates({}, [])


def test_owned_golden_source_has_no_paper_percent() -> None:
    body = _DOMAIN.read_text(encoding="utf-8")
    catalog = _OWNED.read_text(encoding="utf-8")
    assert "96.6" not in body
    assert "96,6" not in body
    assert "92.71" not in body
    assert "96.6" not in catalog
    assert "92.71" not in catalog
