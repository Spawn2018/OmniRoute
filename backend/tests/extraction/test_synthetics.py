"""8–12 syntetyk extract/eval — bez PDF klienta, bez zrzutu PII."""

import subprocess
from pathlib import Path

from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.ai_transforms.extraction.presidio_stub import InstructorPresidioStub
from app.ai_transforms.extraction.synthetics import SYNTHETIC_DOCUMENTS

_REPO_ROOT = Path(__file__).resolve().parents[3]


def test_synthetic_catalog_size() -> None:
    assert 8 <= len(SYNTHETIC_DOCUMENTS) <= 12


def test_synthetics_run_through_mock_extractor() -> None:
    extractor = MockExtractor()
    for source_ref, document in SYNTHETIC_DOCUMENTS:
        assert source_ref.startswith("synth://")
        payload = extractor.extract(source_ref=source_ref, input_text=document)
        dumped = payload.model_dump()
        assert dumped["source_ref"] == source_ref
        assert isinstance(dumped["unparsed_regions"], list)
        assert isinstance(dumped["candidates"], list)
        for candidate in dumped["candidates"]:
            assert candidate["amount_text"]
            assert candidate["code"]
            assert len(candidate["currency"]) == 3


def test_synthetics_pass_instructor_presidio_stub() -> None:
    stub = InstructorPresidioStub()
    for _source_ref, document in SYNTHETIC_DOCUMENTS:
        stub.scan(document)


def test_synthetics_are_not_pdf_and_have_no_pii_dump() -> None:
    stub = InstructorPresidioStub()
    for _source_ref, document in SYNTHETIC_DOCUMENTS:
        assert not document.lstrip().startswith("%PDF")
        assert ".pdf" not in document.lower()
        assert stub.analyze(document) == []


def test_git_has_no_client_pdfs() -> None:
    listed = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.pdf", "**/*.pdf"],
        check=True,
        capture_output=True,
        text=True,
        cwd=_REPO_ROOT,
    )
    assert listed.stdout.strip("\x00").strip() == ""
    product_roots = (
        _REPO_ROOT / "backend",
        _REPO_ROOT / "frontend",
        _REPO_ROOT / "promptfoo",
        _REPO_ROOT / "eval",
    )
    product_pdfs = [
        path
        for root in product_roots
        if root.exists()
        for path in root.rglob("*.pdf")
        if "node_modules" not in path.parts
    ]
    assert product_pdfs == []
