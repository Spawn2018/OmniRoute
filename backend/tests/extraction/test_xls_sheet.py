from pathlib import Path

import pytest

from app.domain.errors import UnparseableDocument
from app.integrations.docling.parser import DeterministicDocumentParser, layout_fingerprint
from app.integrations.docling.xls_sheet import XlsSheetParser

_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_fingerprint_xls_ole() -> None:
    raw = (_FIXTURES / "thc.xls").read_bytes()
    assert layout_fingerprint(raw) == "xls"
    assert layout_fingerprint(b"not-ole") == "text"


def test_xls_sheet_extracts_charge_line() -> None:
    raw = (_FIXTURES / "thc.xls").read_bytes()
    parsed = DeterministicDocumentParser().parse(source_ref="doc://x", raw_bytes=raw)
    assert parsed.parser_name == "xls_sheet"
    assert "THC" in parsed.text
    assert "EUR" in parsed.text


def test_xls_empty_sheet_is_unparseable() -> None:
    raw = (_FIXTURES / "empty.xls").read_bytes()
    with pytest.raises(UnparseableDocument, match="tekstu"):
        XlsSheetParser().parse(source_ref="doc://x", raw_bytes=raw)


def test_xls_parser_requires_ole() -> None:
    with pytest.raises(UnparseableDocument, match="OLE"):
        XlsSheetParser().parse(source_ref="doc://x", raw_bytes=b"PK\x03\x04not-ole")


def test_xls_sheet_index_reads_second_sheet() -> None:
    raw = (_FIXTURES / "two.xls").read_bytes()
    first = XlsSheetParser().parse(source_ref="doc://x", raw_bytes=raw, sheet_index=0)
    second = XlsSheetParser().parse(source_ref="doc://x", raw_bytes=raw, sheet_index=1)
    assert "BAF" in first.text
    assert "THC" in second.text
    assert "EUR" in second.text


def test_xls_sheet_index_out_of_range() -> None:
    raw = (_FIXTURES / "two.xls").read_bytes()
    with pytest.raises(UnparseableDocument, match="sheet_index"):
        XlsSheetParser().parse(source_ref="doc://x", raw_bytes=raw, sheet_index=9)
