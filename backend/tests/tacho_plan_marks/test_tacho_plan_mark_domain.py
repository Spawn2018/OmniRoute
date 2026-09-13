import pytest

from app.domain.errors import InvalidTachoPlanMark
from app.domain.tacho_plan_mark import parse_tacho_plan_mark_row


def test_parse_tacho_plan_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_tacho_plan_mark_row(
        "tpm_plan_01",
        "Plan",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("tpm_plan_01", "plan", "tenant:manual")


def test_parse_tacho_plan_mark_row_rejects_hours_kind() -> None:
    with pytest.raises(InvalidTachoPlanMark, match="rodzaj"):
        parse_tacho_plan_mark_row("tpm_plan_01", "hours", "tenant:manual")
