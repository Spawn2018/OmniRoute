from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_DENIED = "Brak uprawnienia can_manage_geography na organization"
_ENDPOINTS = (
    ("GET", "/api/v1/port-surcharges", None, None),
    (
        "GET",
        "/api/v1/port-surcharges/resolve",
        {"port_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "code": "thc"},
        None,
    ),
    (
        "POST",
        "/api/v1/port-surcharges",
        None,
        {
            "port_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "code": "thc",
            "title": "THC",
            "applies_when": "weekend",
            "amount": "85.0000",
            "currency": "EUR",
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
def _reset_authz():
    set_authz_checker(None)
    yield
    set_authz_checker(None)


@pytest.mark.parametrize(("method", "path", "params", "json_body"), _ENDPOINTS)
def test_port_surcharge_endpoints_are_forbidden_without_geography(
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


def test_authorization_model_grants_geography_to_organization_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_geography"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_geography_without_charges_relation_for_extras() -> None:
    source = (_ROOT / "authz" / "model.fga").read_text(encoding="utf-8")
    assert "can_manage_geography: member" in source
    assert "can_manage_port_surcharges" not in source
