import pytest

from app.domain.campaign_mark import parse_campaign_mark_row
from app.domain.errors import InvalidCampaignMark


def test_parse_campaign_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_campaign_mark_row(
        "cmp_campaign_01",
        "Campaign",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("cmp_campaign_01", "campaign", "tenant:manual")


def test_parse_campaign_mark_row_rejects_funnel_kind() -> None:
    with pytest.raises(InvalidCampaignMark, match="rodzaj"):
        parse_campaign_mark_row("cmp_campaign_01", "funnel", "tenant:manual")
