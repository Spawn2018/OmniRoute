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


def test_list_terminals_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).get("/api/v1/terminals", headers=bearer_auth_headers())
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_resolve_isps_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).get(
        "/api/v1/terminals/resolve",
        headers=bearer_auth_headers(),
        params={"isps_code": "PLGDY-BCT"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_create_terminal_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).post(
        "/api/v1/terminals",
        headers=bearer_auth_headers(),
        json={
            "port_id": str(uuid4()),
            "name": "BCT Gdynia",
            "isps_code": "PLGDY-BCT",
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED
