from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.core import config
from app.domain.errors import DocumentParserUnavailable, UnparseableDocument
from app.integrations.docling.ab import AbDocumentParser
from app.integrations.docling.parser import (
    DeterministicDocumentParser,
    DocumentText,
    layout_fingerprint,
)
from app.integrations.docling.provider import default_parser
from app.services.extraction.extraction_service import ExtractionService
from tests.extraction.test_xlsx_sheet import _xlsx_bytes

_FAKE_PDF = b"%PDF-1.1\n(THC 10 EUR extra)\n%%EOF"


class _FixedParser:
    def __init__(self, text: str, name: str) -> None:
        self._text = text
        self._name = name

    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
        sheet_name: str | None = None,
    ) -> DocumentText:
        del source_ref, raw_bytes, sheet_index, sheet_name
        return DocumentText(text=self._text, parser_name=self._name)


def test_fingerprint_pdf_vs_text() -> None:
    assert layout_fingerprint(_FAKE_PDF) == "pdf"
    assert layout_fingerprint(b"THC 10 EUR") == "text"
    assert layout_fingerprint(b"PK\x03\x04not-a-zip") == "text"


def test_deterministic_pdf_strings_extracts_charge_line() -> None:
    parsed = DeterministicDocumentParser().parse(source_ref="doc://p", raw_bytes=_FAKE_PDF)
    assert parsed.parser_name == "pdf_strings"
    assert "THC 10 EUR" in parsed.text


def test_ab_picks_longer_text_and_records_delta() -> None:
    parser = AbDocumentParser(_FixedParser("aa", "a"), _FixedParser("bbbb", "b"))
    parsed = parser.parse(source_ref="doc://x", raw_bytes=b"ignored")
    assert parsed.parser_name == "b"
    assert parsed.parser_challenger == "b"
    assert parsed.ab_delta_chars == 2
    assert parsed.text == "bbbb"


def test_ab_falls_back_when_challenger_missing() -> None:
    class _Missing:
        def parse(
            self,
            *,
            source_ref: str,
            raw_bytes: bytes,
            sheet_index: int = 0,
            sheet_name: str | None = None,
        ) -> DocumentText:
            del source_ref, raw_bytes, sheet_index, sheet_name
            raise DocumentParserUnavailable("brak docling")

    parsed = AbDocumentParser(_FixedParser("aa", "a"), _Missing()).parse(
        source_ref="doc://x",
        raw_bytes=b"x",
    )
    assert parsed.parser_name == "a"
    assert parsed.ab_delta_chars is None


def test_docling_mode_requires_package(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "extraction_parser", "docling")
    with pytest.raises(DocumentParserUnavailable, match="docling"):
        default_parser().parse(source_ref="doc://x", raw_bytes=b"THC 1 EUR")


def test_unknown_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "extraction_parser", "marker")
    with pytest.raises(DocumentParserUnavailable, match="Nieznany"):
        default_parser()


def test_ab_mode_without_docling_keeps_parser_a(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "extraction_parser", "ab")
    parsed = default_parser().parse(source_ref="doc://x", raw_bytes=b"THC 10 EUR")
    assert parsed.parser_name == "stub"
    assert parsed.ab_delta_chars is None


@pytest.mark.asyncio
async def test_extract_from_document_stores_parser_name() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = ExtractionService(session, parser=DeterministicDocumentParser())
    draft = await service.extract_from_document(
        organization_id=uuid4(),
        user_id=uuid4(),
        source_ref="doc://p",
        raw_bytes=_FAKE_PDF,
    )
    assert draft.payload["parser_name"] == "pdf_strings"
    assert draft.payload["extract_path"] == "text"
    assert "THC" in draft.payload["candidates"][0]["code"]


@pytest.mark.asyncio
async def test_extract_from_document_image_path_still_uses_text_parser() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = ExtractionService(session, parser=DeterministicDocumentParser())
    draft = await service.extract_from_document(
        organization_id=uuid4(),
        user_id=uuid4(),
        source_ref="doc://p",
        raw_bytes=_FAKE_PDF,
        extract_path="image",
    )
    assert draft.payload["extract_path"] == "image"
    assert draft.payload["parser_name"] == "pdf_strings"


@pytest.mark.asyncio
async def test_extract_from_document_xlsx_stores_parser_name() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = ExtractionService(session, parser=DeterministicDocumentParser())
    draft = await service.extract_from_document(
        organization_id=uuid4(),
        user_id=uuid4(),
        source_ref="doc://xlsx",
        raw_bytes=_xlsx_bytes(),
    )
    assert draft.payload["parser_name"] == "xlsx_sheet"
    assert draft.payload["candidates"][0]["code"] == "THC"


@pytest.mark.asyncio
async def test_extract_from_document_rejects_oversize() -> None:
    session = AsyncMock()
    service = ExtractionService(session, parser=DeterministicDocumentParser())
    with pytest.raises(UnparseableDocument, match="2 MB"):
        await service.extract_from_document(
            organization_id=uuid4(),
            user_id=uuid4(),
            source_ref="doc://p",
            raw_bytes=b"x" * 2_000_001,
        )
