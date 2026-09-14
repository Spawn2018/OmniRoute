import pytest

from app.domain.errors import InvalidStyleCascadeMark
from app.domain.style_cascade_mark import parse_style_cascade_mark_row


def test_parse_style_cascade_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_style_cascade_mark_row(
        "style_user_01",
        "User",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("style_user_01", "user", "tenant:manual")


def test_parse_style_cascade_mark_row_rejects_fidelity_kind() -> None:
    with pytest.raises(InvalidStyleCascadeMark, match="rodzaj"):
        parse_style_cascade_mark_row(
            "style_user_01",
            "fidelity",
            "tenant:manual",
        )
