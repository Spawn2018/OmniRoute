import pytest

from app.domain.crm_link_mark import parse_crm_link_mark_row
from app.domain.errors import InvalidCrmLinkMark


def test_parse_crm_link_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_crm_link_mark_row(
        "crm_link_lead_01",
        "Lead",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("crm_link_lead_01", "lead", "tenant:manual")


def test_parse_crm_link_mark_row_rejects_uuid_kind() -> None:
    with pytest.raises(InvalidCrmLinkMark, match="rodzaj"):
        parse_crm_link_mark_row("crm_link_lead_01", "uuid", "tenant:manual")
