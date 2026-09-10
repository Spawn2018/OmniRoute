import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidVisibilityConnector
from app.domain.visibility_connector import parse_visibility_row


def test_parse_visibility_row_accepts_p44_manual() -> None:
    code, kind, origin = parse_visibility_row("p44_desk_pl", "P44", " tenant:manual ")
    assert (code, kind, origin) == ("p44_desk_pl", "p44", "tenant:manual")


def test_parse_visibility_row_accepts_fixture_prefix() -> None:
    parsed = parse_visibility_row("ocean_watch", "p44", "fixture://visibility/pl-1")
    assert parsed[2] == "fixture://visibility/pl-1"


def test_parse_visibility_row_rejects_bad_code() -> None:
    with pytest.raises(InvalidVisibilityConnector, match="oznaczenie"):
        parse_visibility_row("X", "p44", "tenant:manual")
    with pytest.raises(InvalidVisibilityConnector, match="oznaczenie"):
        parse_visibility_row(1, "p44", "tenant:manual")


@given(st.sampled_from(["", "fourkites", "shippeo", "ais", "live"]))
def test_parse_visibility_row_rejects_foreign_vendors(raw: str) -> None:
    with pytest.raises(InvalidVisibilityConnector, match="system"):
        parse_visibility_row("p44_desk_pl", raw, "tenant:manual")


@given(st.sampled_from(["", "   ", "https://p44.com/x", "fixture://portal/1"]))
def test_parse_visibility_row_rejects_foreign_origin(raw: str) -> None:
    with pytest.raises(InvalidVisibilityConnector, match="obce"):
        parse_visibility_row("p44_desk_pl", "p44", raw)
