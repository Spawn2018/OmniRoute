from app.core.config import settings
from app.domain.errors import DocumentParserUnavailable
from app.integrations.docling.ab import AbDocumentParser
from app.integrations.docling.docling_adapter import DoclingDocumentParser
from app.integrations.docling.parser import DeterministicDocumentParser, DocumentParser


def default_parser() -> DocumentParser:
    name = settings.extraction_parser.strip().lower()
    deterministic = DeterministicDocumentParser()
    if name in {"stub", "deterministic"}:
        return deterministic
    if name == "docling":
        return DoclingDocumentParser()
    if name == "ab":
        return AbDocumentParser(deterministic, DoclingDocumentParser())
    raise DocumentParserUnavailable(f"Nieznany extraction_parser: {name}")
