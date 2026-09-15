"""A/B: parser deterministyczny (A) vs docling (B); metryka = różnica długości tekstu."""

from app.domain.errors import DocumentParserUnavailable
from app.integrations.docling.parser import DocumentParser, DocumentText


class AbDocumentParser:
    def __init__(self, primary: DocumentParser, challenger: DocumentParser) -> None:
        self._primary = primary
        self._challenger = challenger

    def parse(
        self,
        *,
        source_ref: str,
        raw_bytes: bytes,
        sheet_index: int = 0,
    ) -> DocumentText:
        primary = self._primary.parse(
            source_ref=source_ref,
            raw_bytes=raw_bytes,
            sheet_index=sheet_index,
        )
        try:
            challenger = self._challenger.parse(
                source_ref=source_ref,
                raw_bytes=raw_bytes,
                sheet_index=sheet_index,
            )
        except DocumentParserUnavailable:
            return DocumentText(text=primary.text, parser_name=primary.parser_name)

        delta = len(challenger.text) - len(primary.text)
        winner = challenger if len(challenger.text) > len(primary.text) else primary
        return DocumentText(
            text=winner.text,
            parser_name=winner.parser_name,
            parser_challenger=challenger.parser_name,
            ab_delta_chars=delta,
        )
