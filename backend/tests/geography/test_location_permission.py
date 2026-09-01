from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers


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
def _reset_authz():
    set_authz_checker(None)
    yield
    set_authz_checker(None)


_DENIED = "Brak uprawnienia can_manage_geography na organization"


def test_list_locations_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).get("/api/v1/locations", headers=bearer_auth_headers())
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_resolve_postal_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).get(
        "/api/v1/locations/resolve",
        headers=bearer_auth_headers(),
        params={"country_code": "PL", "postal_code": "81-198"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_create_zone_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).post(
        "/api/v1/locations",
        headers=bearer_auth_headers(),
        json={"code": "TROJMIASTO", "name": "Trójmiasto"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_add_zone_member_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).post(
        f"/api/v1/locations/{uuid4()}/members",
        headers=bearer_auth_headers(),
        json={"country_code": "PL", "postal_from": "81000", "postal_to": "81999"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_list_zone_members_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).get(
        f"/api/v1/locations/{uuid4()}/members",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED
