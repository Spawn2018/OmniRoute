from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from app.domain.errors import UnparseableDocument
from app.integrations.docling.parser import DeterministicDocumentParser, layout_fingerprint
from app.integrations.docling.xlsx_sheet import XlsxSheetParser

_WORKBOOK = """<?xml version="1.0"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>
</workbook>
"""

_SHEET_THC = """<?xml version="1.0"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>THC 10 EUR</t></is></c>
    </row>
  </sheetData>
</worksheet>
"""

_SHEET_EMPTY = """<?xml version="1.0"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData></sheetData>
</worksheet>
"""


def _xlsx_bytes(sheet: str = _SHEET_THC) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("xl/workbook.xml", _WORKBOOK)
        archive.writestr("xl/worksheets/sheet1.xml", sheet)
    return buffer.getvalue()


def _zip_without_workbook() -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("readme.txt", "no sheet")
    return buffer.getvalue()


def test_fingerprint_xlsx_vs_plain_zip() -> None:
    assert layout_fingerprint(_xlsx_bytes()) == "xlsx"
    assert layout_fingerprint(_zip_without_workbook()) == "text"
    assert layout_fingerprint(b"THC 10 EUR") == "text"


def test_xlsx_sheet_extracts_charge_line() -> None:
    parsed = DeterministicDocumentParser().parse(source_ref="doc://x", raw_bytes=_xlsx_bytes())
    assert parsed.parser_name == "xlsx_sheet"
    assert "THC 10 EUR" in parsed.text


def test_xlsx_empty_sheet_is_unparseable() -> None:
    with pytest.raises(UnparseableDocument, match="tekstu"):
        XlsxSheetParser().parse(source_ref="doc://x", raw_bytes=_xlsx_bytes(_SHEET_EMPTY))


def test_xlsx_parser_requires_workbook() -> None:
    with pytest.raises(UnparseableDocument, match="skoroszytu"):
        XlsxSheetParser().parse(source_ref="doc://x", raw_bytes=_zip_without_workbook())
