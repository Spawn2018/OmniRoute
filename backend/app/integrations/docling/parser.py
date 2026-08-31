"""Docling A/B — stub; żywy parser w plasterze 0.9."""

from typing import Protocol


class ParsedDocument(Protocol):
    text: str
    parser_name: str


class DocumentText:
    def __init__(self, text: str, parser_name: str) -> None:
        self.text = text
        self.parser_name = parser_name


class DocumentParser(Protocol):
    def parse(self, *, source_ref: str, raw_bytes: bytes) -> DocumentText:
        ...


class StubDocumentParser:
    """Bez zależności docling — zwraca UTF-8 tekst z bajtów."""

    def parse(self, *, source_ref: str, raw_bytes: bytes) -> DocumentText:
        del source_ref
        return DocumentText(text=raw_bytes.decode("utf-8", errors="replace"), parser_name="stub")
