from datetime import date

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidOrganizationCalendar
from app.domain.organization_calendar import (
    require_calendar_day,
    require_calendar_source_ref,
    require_country_code,
    require_day_kind,
)


def test_calendar_allowlists() -> None:
    assert require_country_code(" pl ") == "PL"
    assert require_calendar_day(date(2026, 9, 7)) == date(2026, 9, 7)
    assert require_day_kind("holiday") == "holiday"
    assert require_day_kind("working") == "working"
    assert require_calendar_source_ref("tenant:manual") == "tenant:manual"


def test_calendar_rejects_weekend_kind_and_loose_country() -> None:
    with pytest.raises(InvalidOrganizationCalendar, match="rodzaj"):
        require_day_kind("weekend")
    with pytest.raises(InvalidOrganizationCalendar, match="kraju"):
        require_country_code("POL")
    with pytest.raises(InvalidOrganizationCalendar, match="obce"):
        require_calendar_source_ref("mailto:ops@example.com")
    with pytest.raises(InvalidOrganizationCalendar, match="datą"):
        require_calendar_day("2026-09-07")


@given(st.sampled_from(["weekend", "rest", "bank_holiday"]))
def test_calendar_kind_is_not_weekday_token(raw: str) -> None:
    with pytest.raises(InvalidOrganizationCalendar, match="rodzaj"):
        require_day_kind(raw)
