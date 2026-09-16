import pytest

from app.domain.errors import InvalidHandoverSbarMark
from app.domain.handover_sbar_mark import parse_handover_sbar_mark_row


def test_parse_handover_sbar_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_handover_sbar_mark_row(
        "sbar_sit_01",
        "Situation",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("sbar_sit_01", "situation", "tenant:manual")


def test_parse_handover_sbar_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidHandoverSbarMark, match="rodzaj"):
        parse_handover_sbar_mark_row(
            "sbar_sit_01",
            "auto_sbar",
            "tenant:manual",
        )


def test_parse_handover_sbar_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidHandoverSbarMark, match="wskazanie"):
        parse_handover_sbar_mark_row(
            "sbar_sit_01",
            "other",
            "http://evil.example/x",
        )
