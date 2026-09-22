import pytest

from app.domain.clone_carry_mark import parse_clone_carry_mark_row
from app.domain.errors import InvalidCloneCarryMark


def test_parse_clone_carry_mark_row_accepts_carry() -> None:
    code, kind, origin = parse_clone_carry_mark_row(
        "carry_on_clone_01",
        "carry",
        "fixture://clone-carry/a",
    )
    assert code == "carry_on_clone_01"
    assert kind == "carry"
    assert origin == "fixture://clone-carry/a"


def test_parse_clone_carry_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidCloneCarryMark, match="carry"):
        parse_clone_carry_mark_row(
            "carry_on_clone_01",
            "auto",
            "tenant:manual",
        )


def test_parse_clone_carry_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidCloneCarryMark, match="obce"):
        parse_clone_carry_mark_row(
            "carry_on_clone_01",
            "held",
            "http://evil",
        )
