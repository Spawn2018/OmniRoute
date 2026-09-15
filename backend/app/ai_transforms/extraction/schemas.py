"""Schemat wyjścia ekstrakcji — wspólny dla MockExtractor i przyszłego instructor."""

from pydantic import BaseModel, Field


class ExtractedChargeCandidate(BaseModel):
    """Kandydat opłaty — nie jest jeszcze charge/rate_line w bazie."""

    code: str = Field(min_length=1, max_length=64)
    amount_text: str = Field(min_length=1, max_length=64)
    currency: str = Field(min_length=3, max_length=3)
    note: str = ""
    bbox_text: str = ""
    confidence_text: str = ""


class ExtractionHistoryEntry(BaseModel):
    """Poprzednia wersja kandydatów w JSONB — nie tabela historii."""

    revision: int
    candidates: list[ExtractedChargeCandidate] = Field(default_factory=list)


class ExtractionPayload(BaseModel):
    """HC-03: source_ref + unparsed_regions obowiązkowe; LLM nie liczy kwot."""

    source_ref: str = Field(min_length=1, max_length=512)
    unparsed_regions: list[str] = Field(default_factory=list)
    candidates: list[ExtractedChargeCandidate] = Field(default_factory=list)
    parser_name: str = "plain"
    parser_challenger: str | None = None
    ab_delta_chars: int | None = None
    revision: int = 0
    extract_path: str = "text"
    history: list[ExtractionHistoryEntry] = Field(default_factory=list)
