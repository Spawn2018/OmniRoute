import pytest

from app.domain.errors import InvalidStyleFidelityMark
from app.domain.style_fidelity_mark import parse_style_fidelity_mark_row


def test_parse_style_fidelity_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_style_fidelity_mark_row(
        "fid_pass_01",
        "Pass",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("fid_pass_01", "pass", "tenant:manual")


def test_parse_style_fidelity_mark_row_rejects_score_kind() -> None:
    with pytest.raises(InvalidStyleFidelityMark, match="rodzaj"):
        parse_style_fidelity_mark_row(
            "fid_pass_01",
            "score_85",
            "tenant:manual",
        )
