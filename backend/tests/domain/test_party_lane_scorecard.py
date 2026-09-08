from decimal import Decimal

import pytest

from app.domain.errors import InvalidPartyScorecard
from app.domain.party_lane_scorecard import (
    lane_scorecard_hint,
    require_lane_window_days,
    required_lane_count,
)


def test_zero_sample_hint_points_to_global_card() -> None:
    assert lane_scorecard_hint(
        sample_size=0,
        answered_inquiry_count=0,
        shipment_count=0,
        cheapest_count=0,
        median_response_hours=None,
        window_days=90,
    ) == "brak historii na tym kierunku — karta globalna / sieć"


def test_populated_hint_uses_counts() -> None:
    text = lane_scorecard_hint(
        sample_size=4,
        answered_inquiry_count=2,
        shipment_count=1,
        cheapest_count=1,
        median_response_hours=Decimal("12.5000"),
        window_days=30,
    )
    assert "próba 4" in text
    assert "odpowiedzi 2" in text
    assert "12.5000" in text


def test_window_days_rejects_out_of_range() -> None:
    with pytest.raises(InvalidPartyScorecard, match="1–365"):
        require_lane_window_days(0)
    with pytest.raises(InvalidPartyScorecard, match="1–365"):
        require_lane_window_days(366)
    assert require_lane_window_days(None) == 90
    assert require_lane_window_days(30) == 30


def test_lane_count_rejects_negative() -> None:
    with pytest.raises(InvalidPartyScorecard, match="ujemne"):
        required_lane_count(-1, "shipment_count")
    assert required_lane_count(None, "shipment_count") == 0
