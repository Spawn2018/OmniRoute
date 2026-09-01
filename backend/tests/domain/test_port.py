from dataclasses import dataclass
from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import (
    AmbiguousPortToken,
    InvalidPortData,
    InvalidPortToken,
    InvalidUnlocode,
    UnknownPort,
)
from app.domain.port import (
    decode_function_flags,
    normalize_port_token,
    normalize_unlocode,
    parse_coordinates,
    select_resolved_port,
)

_UNLOCODE = st.from_regex(r"[A-Z]{2}[A-Z0-9]{3}", fullmatch=True)
_FUNCTION_FLAGS = st.from_regex(r"[0-9-]{8}", fullmatch=True)
_DEGREES = st.integers(min_value=0, max_value=89)
_MINUTES = st.integers(min_value=0, max_value=59)


@dataclass(frozen=True)
class _Candidate:
    unlocode: str
    is_official: bool


def test_normalize_unlocode_uppercases_and_drops_source_spacing() -> None:
    assert normalize_unlocode(" pl gdy ") == "PLGDY"


def test_normalize_unlocode_rejects_code_shorter_than_five_characters() -> None:
    with pytest.raises(InvalidUnlocode, match="5"):
        normalize_unlocode("PLGD")


def test_normalize_unlocode_rejects_digits_in_country_part() -> None:
    with pytest.raises(InvalidUnlocode, match="5"):
        normalize_unlocode("1LGDY")


def test_normalize_unlocode_rejects_non_text() -> None:
    with pytest.raises(InvalidUnlocode, match="tekstem"):
        normalize_unlocode(54)  # type: ignore[arg-type]


@given(code=_UNLOCODE)
def test_normalize_unlocode_is_idempotent_and_case_insensitive(code: str) -> None:
    assert normalize_unlocode(code) == code
    assert normalize_unlocode(code.lower()) == code


def test_normalize_port_token_collapses_inner_whitespace() -> None:
    assert normalize_port_token("  nowy   port ") == "NOWY PORT"


def test_normalize_port_token_rejects_blank_token() -> None:
    with pytest.raises(InvalidPortToken, match="pusty"):
        normalize_port_token("   ")


@given(token=st.from_regex(r"[A-Z]{1,20}", fullmatch=True))
def test_normalize_port_token_is_idempotent(token: str) -> None:
    assert normalize_port_token(normalize_port_token(token)) == normalize_port_token(token)


def test_decode_function_flags_maps_classifier_positions_to_names() -> None:
    assert decode_function_flags("12-4-6--") == ["port", "rail", "airport", "icd"]


def test_decode_function_flags_ignores_positions_outside_the_model() -> None:
    assert decode_function_flags("--3---7-") == []


def test_decode_function_flags_rejects_classifier_of_wrong_length() -> None:
    with pytest.raises(InvalidPortData, match="8"):
        decode_function_flags("12-4")


@given(classifier=_FUNCTION_FLAGS)
def test_decode_function_flags_returns_known_names_without_duplicates(classifier: str) -> None:
    flags = decode_function_flags(classifier)
    assert set(flags) <= {"port", "rail", "airport", "icd"}
    assert len(flags) == len(set(flags))


def test_parse_coordinates_returns_decimal_never_float() -> None:
    lat, lng = parse_coordinates("5431N 01833E")
    assert isinstance(lat, Decimal)
    assert isinstance(lng, Decimal)
    assert lat == Decimal("54.516667")
    assert lng == Decimal("18.55")


def test_parse_coordinates_signs_southern_and_western_hemisphere() -> None:
    lat, lng = parse_coordinates("3352S 15112W")
    assert lat == Decimal("-33.866667")
    assert lng == Decimal("-151.2")


def test_parse_coordinates_accepts_record_without_position() -> None:
    assert parse_coordinates("") == (None, None)


def test_parse_coordinates_rejects_malformed_position() -> None:
    with pytest.raises(InvalidPortData, match="współrzędne"):
        parse_coordinates("54.31N 18.33E")


@given(lat_deg=_DEGREES, lat_min=_MINUTES, lng_deg=_DEGREES, lng_min=_MINUTES)
def test_parse_coordinates_stays_inside_geographic_range(
    lat_deg: int,
    lat_min: int,
    lng_deg: int,
    lng_min: int,
) -> None:
    raw = f"{lat_deg:02d}{lat_min:02d}N {lng_deg:03d}{lng_min:02d}E"
    lat, lng = parse_coordinates(raw)
    assert lat is not None and lng is not None
    assert Decimal("-90") <= lat <= Decimal("90")
    assert Decimal("-180") <= lng <= Decimal("180")


def test_select_resolved_port_prefers_unlocode_hit_over_alias_hit() -> None:
    gdansk = _Candidate(unlocode="PLGDN", is_official=True)
    gdynia = _Candidate(unlocode="PLGDY", is_official=True)
    assert select_resolved_port("PLGDY", [gdansk, gdynia]) is gdynia


def test_select_resolved_port_prefers_official_row_when_only_aliases_match() -> None:
    manual = _Candidate(unlocode="PLGDN", is_official=False)
    official = _Candidate(unlocode="PLGDY", is_official=True)
    assert select_resolved_port("GDINGEN", [manual, official]) is official


def test_select_resolved_port_rejects_alias_shared_by_two_official_ports() -> None:
    with pytest.raises(AmbiguousPortToken, match="GDINGEN"):
        select_resolved_port(
            "GDINGEN",
            [
                _Candidate(unlocode="PLGDY", is_official=True),
                _Candidate(unlocode="DEGDY", is_official=True),
            ],
        )


def test_select_resolved_port_rejects_token_without_candidates() -> None:
    with pytest.raises(UnknownPort, match="GDINGEN"):
        select_resolved_port("GDINGEN", [])
