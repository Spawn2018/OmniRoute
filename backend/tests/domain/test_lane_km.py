from decimal import Decimal

import pytest

from app.domain.errors import InvalidLaneKm
from app.domain.lane_km import require_km_code, require_lane_km, require_lane_source_ref


def test_km_code_accepts_snake() -> None:
    assert require_km_code("backhaul_a") == "backhaul_a"


def test_km_code_rejects_bad_token() -> None:
    with pytest.raises(InvalidLaneKm, match="oznaczenie"):
        require_km_code("X")
    with pytest.raises(InvalidLaneKm, match="oznaczenie"):
        require_km_code(1)


def test_lane_km_keeps_zero_and_quantizes() -> None:
    assert require_lane_km(0, "ladowny") == Decimal("0.0000")
    assert require_lane_km("12.5", "pusty") == Decimal("12.5000")
    assert require_lane_km(15, "dolot") == Decimal("15.0000")


def test_lane_km_rejects_float_bool_and_negative() -> None:
    with pytest.raises(InvalidLaneKm, match="ladowny"):
        require_lane_km(1.5, "ladowny")
    with pytest.raises(InvalidLaneKm, match="pusty"):
        require_lane_km(True, "pusty")
    with pytest.raises(InvalidLaneKm, match="dolot"):
        require_lane_km("-1", "dolot")


def test_lane_source_ref_accepts_manual_and_fixture() -> None:
    assert require_lane_source_ref("tenant:manual") == "tenant:manual"
    assert require_lane_source_ref("fixture://lane-km/1") == "fixture://lane-km/1"


def test_lane_source_ref_rejects_foreign() -> None:
    with pytest.raises(InvalidLaneKm, match="obce"):
        require_lane_source_ref("http://hold.example/x")
