from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidGroupageTariff
from app.domain.groupage_tariff import (
    require_chargeable_weight,
    require_postal_zone_kind,
    require_tariff_amount,
    require_tariff_code,
    require_tariff_currency,
    require_tariff_source_ref,
    require_tariff_volume_m3,
)
from app.domain.location import LocationKind


@given(st.sampled_from(["zone_a", "ltl_100", "band_west"]))
def test_tariff_code_normalizes_snake(raw: str) -> None:
    assert require_tariff_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_tariff_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidGroupageTariff, match="snake"):
        require_tariff_code(raw)


def test_postal_zone_kind_allows_zone() -> None:
    assert require_postal_zone_kind(LocationKind.POSTAL_ZONE.value) == "postal_zone"


@given(st.sampled_from([LocationKind.UNLOCODE.value, LocationKind.ADDRESS.value]))
def test_postal_zone_kind_rejects_other(kind: str) -> None:
    with pytest.raises(InvalidGroupageTariff, match="strefa"):
        require_postal_zone_kind(kind)


def test_chargeable_weight_rejects_float() -> None:
    with pytest.raises(InvalidGroupageTariff, match="float"):
        require_chargeable_weight(12.5)  # type: ignore[arg-type]


def test_tariff_amount_rejects_float() -> None:
    with pytest.raises(InvalidGroupageTariff, match="float"):
        require_tariff_amount(12.5)  # type: ignore[arg-type]


def test_chargeable_weight_rejects_zero() -> None:
    with pytest.raises(InvalidGroupageTariff, match="dodatnia"):
        require_chargeable_weight("0")


def test_tariff_amount_rejects_zero() -> None:
    with pytest.raises(InvalidGroupageTariff, match="dodatnia"):
        require_tariff_amount("0")


_POSITIVE = st.decimals(
    min_value="0.0001",
    max_value="9999",
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


@given(_POSITIVE)
def test_positive_decimals_quantize(units: Decimal) -> None:
    assert require_chargeable_weight(units) == units
    assert require_tariff_amount(str(units)) == units


def test_tariff_volume_is_optional_positive_decimal() -> None:
    assert require_tariff_volume_m3(None) is None
    assert require_tariff_volume_m3("  ") is None
    assert require_tariff_volume_m3("1.5") == Decimal("1.5000")
    with pytest.raises(InvalidGroupageTariff, match="objętość"):
        require_tariff_volume_m3("-1")
    with pytest.raises(InvalidGroupageTariff, match="objętość"):
        require_tariff_volume_m3(1.5)  # type: ignore[arg-type]


def test_tariff_currency_iso() -> None:
    assert require_tariff_currency("eur") == "EUR"


def test_tariff_source_ref_accepts_fixture() -> None:
    assert (
        require_tariff_source_ref(" fixture://groupage-tariff/1 ")
        == "fixture://groupage-tariff/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_tariff_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidGroupageTariff):
        require_tariff_source_ref(raw)
