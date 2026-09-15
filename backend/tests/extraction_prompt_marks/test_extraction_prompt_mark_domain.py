import pytest

from app.domain.errors import InvalidExtractionPromptMark
from app.domain.extraction_prompt_mark import parse_extraction_prompt_mark_row


def test_parse_extraction_prompt_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_extraction_prompt_mark_row(
        "extract_prompt_01",
        "Extract",
        "tenant:manual",
    )
    assert code == "extract_prompt_01"
    assert kind == "extract"
    assert origin == "tenant:manual"


def test_parse_extraction_prompt_mark_row_rejects_unknown_kind() -> None:
    with pytest.raises(InvalidExtractionPromptMark, match="prompt_kind"):
        parse_extraction_prompt_mark_row("extract_prompt_01", "instructor", "tenant:manual")
