from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_organization_settings na organization"
_ENDPOINTS = (
    (
        "GET",
        "/api/v1/organization-calendars",
        {"country_code": "PL"},
        None,
    ),
    (
        "GET",
        "/api/v1/organization-calendars/working-day",
        {"country_code": "PL", "calendar_day": "2026-09-08"},
        None,
    ),
    (
        "POST",
        "/api/v1/organization-calendars",
        None,
        {
            "country_code": "PL",
            "calendar_day": "2026-09-04",
            "day_kind": "holiday",
            "source_ref": "tenant:manual",
        },
    ),
)


class DenyAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return False


@pytest.fixture(autouse=True)
def _reset_authz() -> object:
    set_authz_checker(None)
    yield
    set_authz_checker(None)


@pytest.mark.parametrize(("method", "path", "params", "json_body"), _ENDPOINTS)
def test_calendar_endpoints_are_forbidden_without_permission(
    method: str,
    path: str,
    params: dict[str, str] | None,
    json_body: dict[str, object] | None,
) -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).request(
        method,
        path,
        headers=bearer_auth_headers(),
        params=params,
        json=json_body,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED
