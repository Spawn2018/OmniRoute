"""Parsery dokumentów: fingerprint + warstwa deterministyczna (CI bez docling)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO
from typing import Protocol
from zipfile import BadZipFile, ZipFile

from app.domain.errors import UnparseableDocument

_PRINTABLE_RUN = re.compile(rb"[\x20-\x7e]{4,}")


@dataclass(frozen=True)
class DocumentText:
    text: str
    parser_name: str
    parser_challenger: str | None = None
    ab_delta_chars: int | None = None


class DocumentParser(Protocol):
    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
        sheet_name: str | None = None,
    ) -> DocumentText: ...


def _zip_has_workbook(raw_bytes: bytes) -> bool:
    try:
        names = ZipFile(BytesIO(raw_bytes)).namelist()
    except BadZipFile:
        return False
    return "xl/workbook.xml" in names


def layout_fingerprint(raw_bytes: bytes) -> str:
    if raw_bytes.startswith(b"%PDF"):
        return "pdf"
    if raw_bytes.startswith(b"PK") and _zip_has_workbook(raw_bytes):
        return "xlsx"
    from app.integrations.docling.xls_sheet import is_ole_compound

    if is_ole_compound(raw_bytes):
        return "xls"
    return "text"


class StubDocumentParser:
    """UTF-8 z bajtów — cenniki wklejone jako tekst."""

    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
        sheet_name: str | None = None,
    ) -> DocumentText:
        del source_ref, sheet_index, sheet_name
        return DocumentText(text=raw_bytes.decode("utf-8", errors="replace"), parser_name="stub")


class PdfStringsParser:
    """Deterministyczny extractor stringów z PDF — parser A bez ML."""

    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
        sheet_name: str | None = None,
    ) -> DocumentText:
        del source_ref, sheet_index, sheet_name
        chunks = [match.decode("ascii") for match in _PRINTABLE_RUN.findall(raw_bytes)]
        text = "\n".join(chunks).strip()
        if not text:
            raise UnparseableDocument("PDF bez wyodrębnionego tekstu")
        return DocumentText(text=text, parser_name="pdf_strings")


class DeterministicDocumentParser:
    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
        sheet_name: str | None = None,
    ) -> DocumentText:
        kind = layout_fingerprint(raw_bytes)
        if kind == "pdf":
            return PdfStringsParser().parse(
                source_ref=source_ref,
                raw_bytes=raw_bytes,
                sheet_index=sheet_index,
                sheet_name=sheet_name,
            )
        if kind == "xlsx":
            from app.integrations.docling.xlsx_sheet import XlsxSheetParser

            return XlsxSheetParser().parse(
                source_ref=source_ref,
                raw_bytes=raw_bytes,
                sheet_index=sheet_index,
                sheet_name=sheet_name,
            )
        if kind == "xls":
            from app.integrations.docling.xls_sheet import XlsSheetParser

            return XlsSheetParser().parse(
                source_ref=source_ref,
                raw_bytes=raw_bytes,
                sheet_index=sheet_index,
                sheet_name=sheet_name,
            )
        return StubDocumentParser().parse(
            source_ref=source_ref,
            raw_bytes=raw_bytes,
            sheet_index=sheet_index,
            sheet_name=sheet_name,
        )
