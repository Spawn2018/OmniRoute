import pytest

from app.domain.errors import InvalidTask
from app.domain.task import parse_task_row


def test_parse_task_row_accepts_valid() -> None:
    code, template, status, origin = parse_task_row(
        "gate_check_01",
        "gate_in",
        "open",
        "tenant:manual",
    )
    assert code == "gate_check_01"
    assert template == "gate_in"
    assert status == "open"
    assert origin == "tenant:manual"


def test_parse_task_row_rejects_bad_code() -> None:
    with pytest.raises(InvalidTask, match="zadanie"):
        parse_task_row("Gate Check", "gate_in", "open", "tenant:manual")


def test_parse_task_row_rejects_bad_status() -> None:
    with pytest.raises(InvalidTask, match="status"):
        parse_task_row("gate_check_01", "gate_in", "closed", "tenant:manual")


def test_parse_task_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidTask, match="obce"):
        parse_task_row(
            "gate_check_01",
            "gate_in",
            "open",
            "http://tasks.example/x",
        )
