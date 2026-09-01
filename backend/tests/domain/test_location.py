import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import (
    InvalidLocationData,
    InvalidPostalCode,
    InvalidPostalRange,
)
from app.domain.location import (
    LocationKind,
    normalize_location_name,
    normalize_postal_bounds,
    normalize_postal_code,
    normalize_zone_code,
    parse_location_kind,
)

_POSTAL = st.from_regex(r"[A-Z0-9]{2,10}", fullmatch=True)


def test_parse_location_kind_accepts_the_three_kinds_of_this_slice() -> None:
    assert parse_location_kind("unlocode") is LocationKind.UNLOCODE
    assert parse_location_kind(" Postal_Zone ") is LocationKind.POSTAL_ZONE
    assert parse_location_kind("ADDRESS") is LocationKind.ADDRESS


def test_parse_location_kind_rejects_terminal_until_the_next_slice() -> None:
    with pytest.raises(InvalidLocationData, match="rodzaj"):
        parse_location_kind("terminal")


def test_normalize_postal_code_drops_separators_used_by_carriers() -> None:
    assert normalize_postal_code("81-198") == "81198"
    assert normalize_postal_code(" sw1a 1aa ") == "SW1A1AA"


def test_normalize_postal_code_rejects_a_loose_place_name() -> None:
    with pytest.raises(InvalidPostalCode, match="kod pocztowy"):
        normalize_postal_code("Gdynia Chylonia")


def test_normalize_postal_bounds_rejects_ends_of_different_length() -> None:
    with pytest.raises(InvalidPostalRange, match="długość"):
        normalize_postal_bounds("81000", "819999")


def test_normalize_postal_bounds_rejects_reversed_range() -> None:
    with pytest.raises(InvalidPostalRange, match="odwrócony"):
        normalize_postal_bounds("81-999", "81-000")


def test_normalize_postal_bounds_accepts_a_single_code_range() -> None:
    assert normalize_postal_bounds("81-198", "81-198") == ("81198", "81198")


def test_normalize_zone_code_folds_spacing_into_underscore() -> None:
    assert normalize_zone_code(" trojmiasto strefa ") == "TROJMIASTO_STREFA"


def test_normalize_location_name_rejects_blank_label() -> None:
    with pytest.raises(InvalidLocationData, match="wymagana"):
        normalize_location_name("   ")


@given(_POSTAL, _POSTAL)
def test_normalized_bounds_are_ordered_or_rejected(left: str, right: str) -> None:
    if len(left) != len(right):
        with pytest.raises(InvalidPostalRange):
            normalize_postal_bounds(left, right)
        return
    lower, upper = normalize_postal_bounds(*sorted((left, right)))
    assert lower <= upper
