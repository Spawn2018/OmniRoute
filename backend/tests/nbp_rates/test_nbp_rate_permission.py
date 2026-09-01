from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_DENIED = "Brak uprawnienia can_manage_nbp_rates na organization"
_ENDPOINTS = (
    ("GET", "/api/v1/nbp-rates", None, None),
    ("GET", "/api/v1/nbp-rates/resolve", {"currency": "EUR", "on_date": "2026-09-01"}, None),
    (
        "POST",
        "/api/v1/nbp-rates",
        None,
        {"currency": "EUR", "rate_date": "2026-09-01", "mid": "4.2500"},
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
def test_nbp_rate_endpoints_are_forbidden_without_permission(
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


def test_authorization_model_grants_nbp_rates_to_organization_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_nbp_rates"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_nbp_rates_relation() -> None:
    source = (_ROOT / "authz" / "model.fga").read_text(encoding="utf-8")
    assert "can_manage_nbp_rates: member" in source
