from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidLocalCharge
from app.domain.local_charge import (
    require_levy_amount,
    require_levy_carrier_label,
    require_levy_currency,
    require_levy_iso,
    require_levy_kind,
    require_levy_port,
    require_levy_service_label,
    require_levy_source_ref,
)


@given(st.sampled_from(["thc", "isps", "seal", "amendment", "THC"]))
def test_levy_kind_normalizes_allowlist(raw: str) -> None:
    assert require_levy_kind(raw) == raw.strip().lower()


@given(st.sampled_from(["", "thc2", "oil"]))
def test_levy_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidLocalCharge, match="rodzaj"):
        require_levy_kind(raw)


def test_levy_amount_rejects_float() -> None:
    with pytest.raises(InvalidLocalCharge, match="kwota"):
        require_levy_amount(12.5)  # type: ignore[arg-type]


def test_levy_amount_rejects_zero() -> None:
    with pytest.raises(InvalidLocalCharge, match="kwota"):
        require_levy_amount("0")


_POSITIVE = st.decimals(
    min_value="0.0001",
    max_value="9999",
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


@given(_POSITIVE)
def test_levy_amount_quantizes(units: Decimal) -> None:
    assert require_levy_amount(str(units)) == units


def test_levy_currency_iso() -> None:
    assert require_levy_currency("eur") == "EUR"


def test_levy_source_ref_accepts_fixture() -> None:
    assert require_levy_source_ref(" fixture://local-charge/1 ") == "fixture://local-charge/1"


def test_levy_port_normalizes_unlocode() -> None:
    assert require_levy_port(" plgdy ") == "PLGDY"
    assert require_levy_port(None) is None
    assert require_levy_port("") is None


def test_levy_port_rejects_short_token() -> None:
    with pytest.raises(InvalidLocalCharge, match="port"):
        require_levy_port("XX")


def test_levy_iso_normalizes_size_type() -> None:
    assert require_levy_iso(" 22g1 ") == "22G1"
    assert require_levy_iso(None) is None
    assert require_levy_iso("") is None


def test_levy_iso_rejects_box_token() -> None:
    with pytest.raises(InvalidLocalCharge, match="typ"):
        require_levy_iso("BOX")


def test_levy_carrier_label_trims() -> None:
    assert require_levy_carrier_label(" MSC ") == "MSC"
    assert require_levy_carrier_label(None) is None
    assert require_levy_carrier_label("") is None


def test_levy_carrier_label_rejects_long() -> None:
    with pytest.raises(InvalidLocalCharge, match="armator"):
        require_levy_carrier_label("x" * 65)


def test_levy_service_label_trims() -> None:
    assert require_levy_service_label(" AE1 ") == "AE1"
    assert require_levy_service_label(None) is None
    assert require_levy_service_label("") is None


def test_levy_service_label_rejects_non_text() -> None:
    with pytest.raises(InvalidLocalCharge, match="serwis"):
        require_levy_service_label(12)  # type: ignore[arg-type]


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_levy_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidLocalCharge):
        require_levy_source_ref(raw)
