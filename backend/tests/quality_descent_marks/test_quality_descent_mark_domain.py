import pytest

from app.domain.errors import InvalidQualityDescentMark
from app.domain.quality_descent_mark import parse_quality_descent_mark_row


def test_parse_quality_descent_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_quality_descent_mark_row(
        "qd_mae_01",
        "Mae",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("qd_mae_01", "mae", "tenant:manual")


def test_parse_quality_descent_mark_row_rejects_score_kind() -> None:
    with pytest.raises(InvalidQualityDescentMark, match="rodzaj"):
        parse_quality_descent_mark_row(
            "qd_mae_01",
            "auto_drop",
            "tenant:manual",
        )
