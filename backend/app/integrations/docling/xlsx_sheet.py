"""Arkusz OOXML → tekst przez openpyxl. Kwoty zostają tekstem z komórki."""

from io import BytesIO
from zipfile import BadZipFile, ZipFile

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.workbook.workbook import Workbook

from app.domain.errors import UnparseableDocument
from app.integrations.docling.parser import DocumentText


def _workbook_has_sheet_xml(raw_bytes: bytes) -> bool:
    try:
        names = ZipFile(BytesIO(raw_bytes)).namelist()
    except BadZipFile:
        return False
    return "xl/workbook.xml" in names


def _load_book(raw_bytes: bytes) -> Workbook:
    try:
        return load_workbook(BytesIO(raw_bytes), data_only=True, read_only=True)
    except (InvalidFileException, OSError, KeyError) as exc:
        raise UnparseableDocument("xlsx nieczytelne") from exc


class XlsxSheetParser:
    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
        sheet_name: str | None = None,
    ) -> DocumentText:
        del source_ref
        if sheet_index < 0:
            raise UnparseableDocument("sheet_index poza zakresem")
        if not _workbook_has_sheet_xml(raw_bytes):
            raise UnparseableDocument("xlsx bez skoroszytu")
        book = _load_book(raw_bytes)

        if sheet_name is not None:
            if sheet_name not in book.sheetnames:
                raise UnparseableDocument("sheet_name poza zakresem")
            rows = book[sheet_name].iter_rows(values_only=True)
        else:
            if sheet_index >= len(book.worksheets):
                raise UnparseableDocument("sheet_index poza zakresem")
            rows = book.worksheets[sheet_index].iter_rows(values_only=True)

        lines: list[str] = []
        for row in rows:
            parts = [
                str(cell).strip()
                for cell in row
                if cell is not None and str(cell).strip() != ""
            ]
            if parts:
                lines.append(" ".join(parts))
        text = "\n".join(lines).strip()
        if not text:
            raise UnparseableDocument("xlsx bez tekstu")
        return DocumentText(text=text, parser_name="xlsx_sheet")
