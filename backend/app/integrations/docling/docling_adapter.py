"""Adapter docling — opcjonalny pakiet, nie w CI."""

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

from app.domain.errors import DocumentParserUnavailable, UnparseableDocument
from app.integrations.docling.parser import DocumentText


class DoclingDocumentParser:
    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
        sheet_name: str | None = None,
    ) -> DocumentText:
        del source_ref, sheet_index, sheet_name
        try:
            from docling.document_converter import DocumentConverter
        except ImportError as exc:
            raise DocumentParserUnavailable(
                "EXTRACTION_PARSER=docling wymaga pakietu docling (pip install -e '.[parsers]')",
            ) from exc

        suffix = ".pdf" if raw_bytes.startswith(b"%PDF") else ".txt"
        tmp_path: str | None = None
        try:
            with NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(raw_bytes)
                tmp_path = tmp.name
            converter = DocumentConverter()
            exported = converter.convert(tmp_path).document.export_to_text()
        finally:
            if tmp_path is not None:
                Path(tmp_path).unlink(missing_ok=True)

        text = exported.strip()
        if not text:
            raise UnparseableDocument("docling zwrócił pusty tekst")
        return DocumentText(text=text, parser_name="docling")
