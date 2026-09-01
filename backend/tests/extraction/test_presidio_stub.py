"""Presidio = stub na instructor. Nie middleware, nie każdy endpoint."""

from pathlib import Path

import pytest

from app.ai_transforms.extraction.instructor_extractor import InstructorExtractor
from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.ai_transforms.extraction.presidio_stub import InstructorPresidioStub
from app.ai_transforms.extraction.schemas import ExtractedChargeCandidate, ExtractionPayload
from app.domain.errors import UntrustedExtractionInput
from app.services.extraction import extraction_service as extraction_service_mod

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_APP_ROOT = _BACKEND_ROOT / "app"


def _clean_payload() -> ExtractionPayload:
    return ExtractionPayload(
        source_ref="hallucinated://model",
        unparsed_regions=[],
        candidates=[
            ExtractedChargeCandidate(code="THC", amount_text="10", currency="EUR"),
        ],
    )


def test_presidio_engine_is_stub_not_live_package() -> None:
    assert InstructorPresidioStub.engine == "stub"
    source = (_APP_ROOT / "ai_transforms" / "extraction" / "presidio_stub.py").read_text(
        encoding="utf-8",
    )
    assert "from presidio" not in source
    assert "import presidio" not in source
    assert "AnalyzerEngine" not in source


def test_instructor_presidio_blocks_email_before_complete() -> None:
    def complete(_source_ref: str, _input_text: str) -> ExtractionPayload:
        raise AssertionError("complete called after PII")

    leaked = "operator@example.test"
    extractor = InstructorExtractor(complete=complete)
    with pytest.raises(UntrustedExtractionInput, match="presidio_stub") as caught:
        extractor.extract(source_ref="synth://x", input_text=f"THC 10 EUR {leaked}")
    assert leaked not in str(caught.value)


def test_instructor_presidio_blocks_phone_without_echoing() -> None:
    def complete(_source_ref: str, _input_text: str) -> ExtractionPayload:
        raise AssertionError("complete called after PII")

    leaked = "+48 600 100 200"
    extractor = InstructorExtractor(complete=complete)
    with pytest.raises(UntrustedExtractionInput, match="PHONE_NUMBER") as caught:
        extractor.extract(source_ref="synth://x", input_text=f"THC 10 EUR tel {leaked}")
    assert leaked not in str(caught.value)


def test_instructor_presidio_allows_tariff_text() -> None:
    extractor = InstructorExtractor(complete=lambda _ref, _text: _clean_payload())
    payload = extractor.extract(source_ref="synth://thc", input_text="THC 10 EUR")
    assert payload.source_ref == "synth://thc"
    assert payload.candidates[0].amount_text == "10"


def test_mock_extractor_does_not_run_presidio() -> None:
    payload = MockExtractor().extract(
        source_ref="synth://x",
        input_text="THC 10 EUR operator@example.test",
    )
    assert payload.candidates[0].code == "THC"
    assert any("example.test" in region for region in payload.unparsed_regions)


def test_http_surface_has_no_presidio() -> None:
    surfaces = [_APP_ROOT / "main.py", *(_APP_ROOT / "api").rglob("*.py")]
    offenders = [
        path.as_posix()
        for path in surfaces
        if "presidio" in path.read_text(encoding="utf-8").lower()
    ]
    assert offenders == []


def test_presidio_stub_only_wired_on_instructor() -> None:
    callers: list[str] = []
    for path in _APP_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "InstructorPresidioStub" in text or "presidio_stub" in text:
            callers.append(path.relative_to(_APP_ROOT).as_posix())
    assert sorted(callers) == [
        "ai_transforms/extraction/instructor_extractor.py",
        "ai_transforms/extraction/presidio_stub.py",
    ]


def test_extraction_service_still_does_not_import_rates() -> None:
    assert not hasattr(extraction_service_mod, "RateLineService")
    assert not hasattr(extraction_service_mod, "RateLine")
    source = (_APP_ROOT / "services" / "extraction" / "extraction_service.py").read_text(
        encoding="utf-8",
    )
    assert "from app.services.rate_lines" not in source
    assert "from app.models.rate_line" not in source
    assert "presidio" not in source.lower()
