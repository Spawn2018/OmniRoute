import pytest

from app.domain.crm_opportunity import parse_crm_opportunity_row
from app.domain.errors import InvalidCrmOpportunity


def test_parse_crm_opportunity_row_accepts_manual() -> None:
    code, kind, origin = parse_crm_opportunity_row(
        "opp_acme_01",
        "Open",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("opp_acme_01", "open", "tenant:manual")


def test_parse_crm_opportunity_row_rejects_pipeline_kind() -> None:
    with pytest.raises(InvalidCrmOpportunity, match="rodzaj"):
        parse_crm_opportunity_row("opp_acme_01", "pipeline", "tenant:manual")
