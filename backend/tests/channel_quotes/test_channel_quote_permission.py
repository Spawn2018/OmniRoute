from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_DENIED = "Brak uprawnienia can_manage_rate_lines na organization"
_ENDPOINTS = (
    ("GET", "/api/v1/channel-quotes", None, None),
    (
        "GET",
        "/api/v1/channel-quotes/resolve",
        {
            "party_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "origin_port_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "destination_port_id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "on_date": "2026-09-01",
        },
        None,
    ),
    (
        "POST",
        "/api/v1/channel-quotes",
        None,
        {
            "party_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "origin_port_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "destination_port_id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "quote_date": "2026-09-01",
            "amount": "1200.0000",
            "currency": "USD",
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
def test_channel_quote_endpoints_are_forbidden_without_rate_lines(
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


def test_authorization_model_grants_rate_lines_to_organization_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_rate_lines"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_reuses_rate_lines_without_new_channel_relation() -> None:
    source = (_ROOT / "authz" / "model.fga").read_text(encoding="utf-8")
    assert "can_manage_rate_lines: member" in source
    assert "can_manage_channel_quotes" not in source
