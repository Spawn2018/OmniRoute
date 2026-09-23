from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_DENIED = "Brak uprawnienia can_manage_dangerous_goods na organization"
_ENDPOINTS = (
    ("GET", "/api/v1/dangerous-goods", None, None),
    ("GET", "/api/v1/dangerous-goods/resolve", {"token": "1203"}, None),
    (
        "POST",
        "/api/v1/dangerous-goods",
        None,
        {
            "un_number": "1203",
            "imdg_class": "3",
            "name": "Petrol",
            "aliases": [],
            "adr_tunnel_code": "D",
            "segregation_group": "none",
            "packing_group": "II",
            "marine_pollutant": False,
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
def test_dangerous_good_endpoints_are_forbidden_without_permission(
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


def test_authorization_model_grants_dangerous_goods_to_organization_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_dangerous_goods"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_dangerous_goods_relation() -> None:
    source = (_ROOT / "authz" / "model.fga").read_text(encoding="utf-8")
    assert "can_manage_dangerous_goods: member" in source
