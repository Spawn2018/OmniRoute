import pytest

from app.domain.errors import InvalidTripVarianceMark
from app.domain.trip_variance_mark import parse_trip_variance_mark_row


def test_parse_trip_variance_mark_row_accepts_expected() -> None:
    code, kind, origin = parse_trip_variance_mark_row(
        "var_expected_01",
        "expected",
        "fixture://trip-variance/a",
    )
    assert code == "var_expected_01"
    assert kind == "expected"
    assert origin == "fixture://trip-variance/a"


def test_parse_trip_variance_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidTripVarianceMark, match="wariancja"):
        parse_trip_variance_mark_row(
            "var_expected_01",
            "live",
            "tenant:manual",
        )


def test_parse_trip_variance_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidTripVarianceMark, match="obce"):
        parse_trip_variance_mark_row(
            "var_expected_01",
            "expected",
            "http://evil",
        )
