"""Pierwszy lub wskazany arkusz OOXML → tekst. Bez openpyxl. Kwoty zostają tekstem z XML."""

from io import BytesIO
from xml.etree.ElementTree import Element, fromstring
from zipfile import BadZipFile, ZipFile

from app.domain.errors import UnparseableDocument
from app.integrations.docling.parser import DocumentText


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _shared_strings(archive: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = fromstring(archive.read("xl/sharedStrings.xml"))
    values: list[str] = []
    for item in root:
        if _local(item.tag) != "si":
            continue
        values.append("".join(node.text or "" for node in item.iter() if _local(node.tag) == "t"))
    return values


def _cell_text(cell: Element, shared: list[str]) -> str:
    kind = cell.get("t")
    if kind == "inlineStr":
        return "".join(node.text or "" for node in cell.iter() if _local(node.tag) == "t")
    value = ""
    for node in cell:
        if _local(node.tag) == "v":
            value = node.text or ""
            break
    if kind == "s":
        index = int(value) if value.isdigit() else -1
        if 0 <= index < len(shared):
            return shared[index]
        return ""
    return value


def _sheet_paths(names: list[str]) -> list[str]:
    numbered = sorted(
        name for name in names if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
    )
    if not numbered:
        raise UnparseableDocument("xlsx bez arkusza")
    return numbered


def _sheet_names(archive: ZipFile) -> list[str]:
    root = fromstring(archive.read("xl/workbook.xml"))
    labels: list[str] = []
    for node in root.iter():
        if _local(node.tag) != "sheet":
            continue
        name = node.get("name")
        if name is None or name.strip() == "":
            continue
        labels.append(name)
    return labels


def _resolve_sheet_path(
    archive: ZipFile,
    names: list[str],
    *,
    sheet_index: int,
    sheet_name: str | None,
) -> str:
    paths = _sheet_paths(names)
    if sheet_name is not None:
        labels = _sheet_names(archive)
        for index, label in enumerate(labels):
            if label == sheet_name and index < len(paths):
                return paths[index]
        raise UnparseableDocument("sheet_name poza zakresem")
    if sheet_index < 0 or sheet_index >= len(paths):
        raise UnparseableDocument("sheet_index poza zakresem")
    return paths[sheet_index]


def _sheet_lines(root: Element, shared: list[str]) -> list[str]:
    lines: list[str] = []
    for row in root.iter():
        if _local(row.tag) != "row":
            continue
        parts = [_cell_text(cell, shared) for cell in row if _local(cell.tag) == "c"]
        line = " ".join(part for part in parts if part.strip())
        if line:
            lines.append(line)
    return lines


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
        try:
            archive = ZipFile(BytesIO(raw_bytes))
        except BadZipFile as exc:
            raise UnparseableDocument("xlsx nieczytelne") from exc
        names = archive.namelist()
        if "xl/workbook.xml" not in names:
            raise UnparseableDocument("xlsx bez skoroszytu")
        path = _resolve_sheet_path(
            archive,
            names,
            sheet_index=sheet_index,
            sheet_name=sheet_name,
        )
        shared = _shared_strings(archive)
        root = fromstring(archive.read(path))
        text = "\n".join(_sheet_lines(root, shared)).strip()
        if not text:
            raise UnparseableDocument("xlsx bez tekstu")
        return DocumentText(text=text, parser_name="xlsx_sheet")
