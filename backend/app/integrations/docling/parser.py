"""Parsery dokumentów: fingerprint + warstwa deterministyczna (CI bez docling)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

from app.domain.errors import UnparseableDocument

_PRINTABLE_RUN = re.compile(rb"[\x20-\x7e]{4,}")


@dataclass(frozen=True)
class DocumentText:
    text: str
    parser_name: str
    parser_challenger: str | None = None
    ab_delta_chars: int | None = None


class DocumentParser(Protocol):
    def parse(self, *, source_ref: str, raw_bytes: bytes) -> DocumentText: ...


def layout_fingerprint(raw_bytes: bytes) -> str:
    if raw_bytes.startswith(b"%PDF"):
        return "pdf"
    return "text"


class StubDocumentParser:
    """UTF-8 z bajtów — cenniki wklejone jako tekst."""

    def parse(self, *, source_ref: str, raw_bytes: bytes) -> DocumentText:
        del source_ref
        return DocumentText(text=raw_bytes.decode("utf-8", errors="replace"), parser_name="stub")


class PdfStringsParser:
    """Deterministyczny extractor stringów z PDF — parser A bez ML."""

    def parse(self, *, source_ref: str, raw_bytes: bytes) -> DocumentText:
        del source_ref
        chunks = [match.decode("ascii") for match in _PRINTABLE_RUN.findall(raw_bytes)]
        text = "\n".join(chunks).strip()
        if not text:
            raise UnparseableDocument("PDF bez wyodrębnionego tekstu")
        return DocumentText(text=text, parser_name="pdf_strings")


class DeterministicDocumentParser:
    def parse(self, *, source_ref: str, raw_bytes: bytes) -> DocumentText:
        if layout_fingerprint(raw_bytes) == "pdf":
            return PdfStringsParser().parse(source_ref=source_ref, raw_bytes=raw_bytes)
        return StubDocumentParser().parse(source_ref=source_ref, raw_bytes=raw_bytes)
