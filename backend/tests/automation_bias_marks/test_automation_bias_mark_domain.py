import pytest

from app.domain.errors import InvalidAutomationBiasMark
from app.domain.automation_bias_mark import parse_automation_bias_mark_row


def test_parse_automation_bias_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_automation_bias_mark_row(
        "ab_confirm_01",
        "Confirm",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("ab_confirm_01", "confirm", "tenant:manual")


def test_parse_automation_bias_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidAutomationBiasMark, match="rodzaj"):
        parse_automation_bias_mark_row(
            "ab_confirm_01",
            "auto_accept",
            "tenant:manual",
        )
