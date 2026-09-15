import pytest

from app.domain.crm_activity import parse_crm_activity_row
from app.domain.errors import InvalidCrmActivity


def test_parse_crm_activity_row_accepts_manual() -> None:
    code, kind, origin = parse_crm_activity_row(
        "act_call_01",
        "Call",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("act_call_01", "call", "tenant:manual")


def test_parse_crm_activity_row_rejects_pipeline_kind() -> None:
    with pytest.raises(InvalidCrmActivity, match="rodzaj"):
        parse_crm_activity_row("act_call_01", "pipeline", "tenant:manual")
