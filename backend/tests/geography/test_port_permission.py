from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]


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


def test_list_ports_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).get("/api/v1/ports", headers=bearer_auth_headers())
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_resolve_port_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).get(
        "/api/v1/ports/resolve",
        headers=bearer_auth_headers(),
        params={"token": "Gdingen"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_create_port_forbidden_without_geography_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).post(
        "/api/v1/ports",
        headers=bearer_auth_headers(),
        json={"unlocode": "PLGDY", "name": "Gdynia", "country_code": "PL"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_authorization_model_grants_geography_to_organization_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_geography"]
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_geography_relation() -> None:
    source = (_ROOT / "authz" / "model.fga").read_text(encoding="utf-8")
    assert "can_manage_geography" in source
