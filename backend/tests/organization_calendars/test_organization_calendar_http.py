from datetime import timedelta
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidOrganizationCalendar, InvalidOrganizationSetting
from app.domain.organization_calendar import (
    require_calendar_day,
    require_calendar_source_ref,
    require_country_code,
    require_day_kind,
)
from app.main import app
from app.models.organization_calendar import OrganizationCalendar
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class StubOrganizationCalendarService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OrganizationCalendar] = []

    async def list_for_country(self, *, country_code: object) -> list[OrganizationCalendar]:
        code = require_country_code(country_code)
        return [
            row
            for row in self.rows
            if row.country_code == code and row.superseded_by is None
        ]

    async def is_working_day(self, *, country_code: object, calendar_day: object) -> bool:
        code = require_country_code(country_code)
        day = require_calendar_day(calendar_day)
        current = next(
            (
                row
                for row in self.rows
                if row.country_code == code
                and row.calendar_day == day
                and row.superseded_by is None
            ),
            None,
        )
        if current is not None:
            return current.day_kind == "working"
        return day.isoweekday() < 6

    async def fx_rate_day(
        self,
        *,
        country_code: object,
        anchor: object,
        offset_days: object,
    ) -> object:
        code = require_country_code(country_code)
        day = require_calendar_day(anchor)
        if type(offset_days) is not str or offset_days.strip() not in {"0", "-1"}:
            raise InvalidOrganizationSetting("dni: tylko 0 albo -1")
        if offset_days.strip() == "0":
            return day
        cursor = day
        for _step in range(14):
            cursor = cursor - timedelta(days=1)
            current = next(
                (
                    row
                    for row in self.rows
                    if row.country_code == code
                    and row.calendar_day == cursor
                    and row.superseded_by is None
                ),
                None,
            )
            if current is not None:
                if current.day_kind == "working":
                    return cursor
                continue
            if cursor.isoweekday() < 6:
                return cursor
        raise InvalidOrganizationCalendar("dni: brak dnia roboczego w oknie")

    async def record_day(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        country_code: object,
        calendar_day: object,
        day_kind: object,
        source_ref: object,
    ) -> OrganizationCalendar:
        code = require_country_code(country_code)
        day = require_calendar_day(calendar_day)
        kind = require_day_kind(day_kind)
        origin = require_calendar_source_ref(source_ref)
        current = next(
            (
                row
                for row in self.rows
                if row.country_code == code
                and row.calendar_day == day
                and row.superseded_by is None
            ),
            None,
        )
        if current is not None and current.day_kind == kind and current.source_ref == origin:
            return current
        successor = OrganizationCalendar(
            id=uuid4(),
            organization_id=organization_id,
            country_code=code,
            calendar_day=day,
            day_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    days = StubOrganizationCalendarService(object())

    def _rows(_session: object) -> StubOrganizationCalendarService:
        return days

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.organization_calendars.OrganizationCalendarService",
        _rows,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), days
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_calendar_day_and_get_by_country(catalog_client: object) -> None:
    client, _days = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/organization-calendars",
        headers=headers,
        json={
            "country_code": "PL",
            "calendar_day": "2026-09-04",
            "day_kind": "holiday",
            "source_ref": "tenant:manual",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["day_kind"] == "holiday"
    assert "amount" not in body
    listed = client.get(
        "/api/v1/organization-calendars",
        headers=headers,
        params={"country_code": "PL"},
    )
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_override_supersedes_and_rejects_weekend_kind(catalog_client: object) -> None:
    client, _days = catalog_client
    headers = bearer_auth_headers()
    payload = {
        "country_code": "PL",
        "calendar_day": "2026-09-04",
        "day_kind": "holiday",
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/organization-calendars", headers=headers, json=payload)
    first_id = first.json()["id"]
    second = client.post(
        "/api/v1/organization-calendars",
        headers=headers,
        json={**payload, "day_kind": "working"},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first_id
    listed = client.get(
        "/api/v1/organization-calendars",
        headers=headers,
        params={"country_code": "PL"},
    )
    assert listed.json()[0]["id"] == second.json()["id"]
    weekend = client.post(
        "/api/v1/organization-calendars",
        headers=headers,
        json={**payload, "day_kind": "weekend"},
    )
    assert weekend.status_code == 400
    assert "rodzaj" in weekend.json()["detail"]


def test_http_working_day_uses_override_not_python_grace(catalog_client: object) -> None:
    client, _days = catalog_client
    headers = bearer_auth_headers()
    friday = client.get(
        "/api/v1/organization-calendars/working-day",
        headers=headers,
        params={"country_code": "PL", "calendar_day": "2026-09-04"},
    )
    assert friday.json()["is_working_day"] is True
    sunday = client.get(
        "/api/v1/organization-calendars/working-day",
        headers=headers,
        params={"country_code": "PL", "calendar_day": "2026-09-06"},
    )
    assert sunday.json()["is_working_day"] is False
    client.post(
        "/api/v1/organization-calendars",
        headers=headers,
        json={
            "country_code": "PL",
            "calendar_day": "2026-09-04",
            "day_kind": "holiday",
            "source_ref": "tenant:manual",
        },
    )
    holiday = client.get(
        "/api/v1/organization-calendars/working-day",
        headers=headers,
        params={"country_code": "PL", "calendar_day": "2026-09-04"},
    )
    assert holiday.json()["is_working_day"] is False
    client.post(
        "/api/v1/organization-calendars",
        headers=headers,
        json={
            "country_code": "PL",
            "calendar_day": "2026-09-06",
            "day_kind": "working",
            "source_ref": "tenant:manual",
        },
    )
    sunday_open = client.get(
        "/api/v1/organization-calendars/working-day",
        headers=headers,
        params={"country_code": "PL", "calendar_day": "2026-09-06"},
    )
    assert sunday_open.json()["is_working_day"] is True


def test_http_fx_rate_day_is_previous_working_day(catalog_client: object) -> None:
    client, _days = catalog_client
    headers = bearer_auth_headers()
    sunday = client.get(
        "/api/v1/organization-calendars/fx-rate-day",
        headers=headers,
        params={"country_code": "PL", "anchor": "2026-09-06", "offset_days": "-1"},
    )
    assert sunday.status_code == 200
    assert sunday.json()["fx_rate_day"] == "2026-09-04"
    same = client.get(
        "/api/v1/organization-calendars/fx-rate-day",
        headers=headers,
        params={"country_code": "PL", "anchor": "2026-09-06", "offset_days": "0"},
    )
    assert same.json()["fx_rate_day"] == "2026-09-06"
    bad = client.get(
        "/api/v1/organization-calendars/fx-rate-day",
        headers=headers,
        params={"country_code": "PL", "anchor": "2026-09-06", "offset_days": "2"},
    )
    assert bad.status_code == 400
    assert "dni" in bad.json()["detail"]
    client.post(
        "/api/v1/organization-calendars",
        headers=headers,
        json={
            "country_code": "PL",
            "calendar_day": "2026-09-04",
            "day_kind": "holiday",
            "source_ref": "tenant:manual",
        },
    )
    shifted = client.get(
        "/api/v1/organization-calendars/fx-rate-day",
        headers=headers,
        params={"country_code": "PL", "anchor": "2026-09-07", "offset_days": "-1"},
    )
    assert shifted.json()["fx_rate_day"] == "2026-09-03"


def test_fx_rate_day_stays_in_sql() -> None:
    root = Path(__file__).resolve().parents[2]
    service = (
        root / "app" / "services" / "organization_calendars" / "organization_calendar_service.py"
    ).read_text(encoding="utf-8")
    repository = (
        root
        / "app"
        / "repositories"
        / "organization_calendars"
        / "organization_calendar_repository.py"
    ).read_text(encoding="utf-8")
    assert ".weekday(" not in service
    assert "isoweekday(" not in service
    assert ".weekday(" not in repository
    assert "isoweekday(" not in repository
    assert "app.services.charges" not in service
    assert "app.services.nbp_rates" not in service
    assert "generate_series(1, 14)" in repository
