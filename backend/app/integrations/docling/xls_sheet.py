"""Pierwszy arkusz BIFF (.xls) → tekst. xlrd tylko BIFF; nie openpyxl."""

from decimal import Decimal, InvalidOperation

import xlrd
from xlrd.biffh import XLRDError
from xlrd.xldate import XLDateError

from app.domain.errors import UnparseableDocument
from app.integrations.docling.parser import DocumentText

_OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def is_ole_compound(raw_bytes: bytes) -> bool:
    return raw_bytes.startswith(_OLE_MAGIC)


def _cell_as_text(book: xlrd.Book, sheet: xlrd.sheet.Sheet, row: int, col: int) -> str:
    cell = sheet.cell(row, col)
    if cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
        return ""
    if cell.ctype == xlrd.XL_CELL_TEXT:
        return str(cell.value).strip()
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        # Kwota zostaje tekstem — nie float w charge; Decimal z repr xlrd.
        try:
            return format(Decimal(str(cell.value)), "f")
        except InvalidOperation:
            return str(cell.value)
    if cell.ctype == xlrd.XL_CELL_DATE:
        raw_date = cell.value
        if type(raw_date) is not float:
            return str(raw_date)
        try:
            stamp = xlrd.xldate_as_datetime(raw_date, book.datemode)
        except (ValueError, OverflowError, XLDateError):
            return str(raw_date)
        return stamp.isoformat(sep=" ", timespec="seconds")
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:
        return "true" if cell.value else "false"
    return str(cell.value).strip()


def _sheet_lines(book: xlrd.Book, sheet: xlrd.sheet.Sheet) -> list[str]:
    lines: list[str] = []
    for row in range(sheet.nrows):
        parts = [_cell_as_text(book, sheet, row, col) for col in range(sheet.ncols)]
        line = " ".join(part for part in parts if part)
        if line:
            lines.append(line)
    return lines


class XlsSheetParser:
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
        if not is_ole_compound(raw_bytes):
            raise UnparseableDocument("xls bez nagłówka OLE")
        try:
            book = xlrd.open_workbook(file_contents=raw_bytes, formatting_info=False)
        except XLRDError as exc:
            raise UnparseableDocument("xls nieczytelne") from exc
        if book.nsheets < 1:
            raise UnparseableDocument("xls bez arkusza")
        if sheet_name is not None:
            try:
                sheet = book.sheet_by_name(sheet_name)
            except XLRDError as exc:
                raise UnparseableDocument("sheet_name poza zakresem") from exc
        else:
            if sheet_index >= book.nsheets:
                raise UnparseableDocument("sheet_index poza zakresem")
            sheet = book.sheet_by_index(sheet_index)
        text = "\n".join(_sheet_lines(book, sheet)).strip()
        if not text:
            raise UnparseableDocument("xls bez tekstu")
        return DocumentText(text=text, parser_name="xls_sheet")
