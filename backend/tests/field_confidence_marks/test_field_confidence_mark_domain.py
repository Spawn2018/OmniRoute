import pytest

from app.domain.errors import InvalidFieldConfidenceMark
from app.domain.field_confidence_mark import parse_field_confidence_mark_row


def test_parse_field_confidence_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_field_confidence_mark_row(
        "fc_green_01",
        "Green",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("fc_green_01", "green", "tenant:manual")


def test_parse_field_confidence_mark_row_rejects_score_kind() -> None:
    with pytest.raises(InvalidFieldConfidenceMark, match="rodzaj"):
        parse_field_confidence_mark_row(
            "fc_green_01",
            "auto_accept",
            "tenant:manual",
        )
