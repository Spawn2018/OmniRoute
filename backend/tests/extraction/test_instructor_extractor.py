import pytest

from app.ai_transforms.extraction.instructor_extractor import InstructorExtractor
from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.ai_transforms.extraction.provider import default_extractor
from app.ai_transforms.extraction.schemas import ExtractedChargeCandidate, ExtractionPayload
from app.core import config
from app.domain.errors import ExtractionProviderUnavailable


def test_instructor_overwrites_source_ref_from_request() -> None:
    def complete(_source_ref: str, _input_text: str) -> ExtractionPayload:
        return ExtractionPayload(
            source_ref="hallucinated://model",
            unparsed_regions=["footer"],
            candidates=[
                ExtractedChargeCandidate(code="THC", amount_text="10", currency="EUR"),
            ],
        )

    extractor = InstructorExtractor(complete=complete)
    payload = extractor.extract(source_ref="tariff://real", input_text="THC 10 EUR")
    assert payload.source_ref == "tariff://real"
    assert payload.unparsed_regions == ["footer"]
    assert payload.candidates[0].amount_text == "10"


def test_from_settings_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "openai_api_key", "")
    with pytest.raises(ExtractionProviderUnavailable, match="OPENAI_API_KEY"):
        InstructorExtractor.from_settings()


def test_default_extractor_is_mock() -> None:
    assert isinstance(default_extractor(), MockExtractor)


def test_unknown_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "extraction_provider", "unknown")
    with pytest.raises(ExtractionProviderUnavailable, match="Nieznany"):
        default_extractor()


def test_instructor_provider_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "extraction_provider", "instructor")
    monkeypatch.setattr(config.settings, "openai_api_key", "")
    with pytest.raises(ExtractionProviderUnavailable, match="OPENAI_API_KEY"):
        default_extractor()
