import json
from pathlib import Path
from typing import Protocol

import pytest

from app.ai_transforms.extraction.instructor_extractor import InstructorExtractor
from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.ai_transforms.extraction.schemas import ExtractionPayload
from app.domain.errors import InvalidExtractionDraft
from app.domain.extraction_draft import unmatched_golden_candidates

_OWNED = Path(__file__).resolve().parent / "golden" / "owned.json"
_DOMAIN = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "domain"
    / "extraction_draft.py"
)


class _Extractor(Protocol):
    def extract(self, *, source_ref: str, input_text: str) -> ExtractionPayload: ...


def _owned_cases() -> list[object]:
    raw = json.loads(_OWNED.read_text(encoding="utf-8"))
    assert type(raw) is list
    assert len(raw) >= 5000
    return raw


def _assert_matches_golden(extractor: _Extractor) -> None:
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


def test_owned_golden_matches_mock_extractor() -> None:
    _assert_matches_golden(MockExtractor())


def test_owned_golden_matches_instructor_stub() -> None:
    # Bramka AI3: ścieżka instructor bez sieci — complete = MockExtractor.
    mock = MockExtractor()

    def complete(source_ref: str, input_text: str) -> ExtractionPayload:
        return mock.extract(source_ref=source_ref, input_text=input_text)

    _assert_matches_golden(InstructorExtractor(complete=complete))


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
