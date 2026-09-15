import pytest

from app.domain.article50_mark import parse_article50_mark_row
from app.domain.errors import InvalidArticle50Mark


def test_parse_article50_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_article50_mark_row(
        "a50_generated_01",
        "Generated",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("a50_generated_01", "generated", "tenant:manual")


def test_parse_article50_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidArticle50Mark, match="rodzaj"):
        parse_article50_mark_row(
            "a50_generated_01",
            "auto_accept",
            "tenant:manual",
        )
