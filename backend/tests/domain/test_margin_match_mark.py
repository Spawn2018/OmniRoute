import pytest

from app.domain.errors import InvalidMarginMatchMark
from app.domain.margin_match_mark import parse_margin_match_mark_row


def test_parse_margin_match_mark_row_accepts_match() -> None:
    code, kind, origin = parse_margin_match_mark_row(
        "var_match_01",
        "match",
        "fixture://margin-match/a",
    )
    assert code == "var_match_01"
    assert kind == "match"
    assert origin == "fixture://margin-match/a"


def test_parse_margin_match_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidMarginMatchMark, match="dopasowanie"):
        parse_margin_match_mark_row(
            "var_match_01",
            "live",
            "tenant:manual",
        )


def test_parse_margin_match_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidMarginMatchMark, match="obce"):
        parse_margin_match_mark_row(
            "var_match_01",
            "match",
            "http://evil",
        )
