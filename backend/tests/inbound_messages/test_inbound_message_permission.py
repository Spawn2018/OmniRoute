from pathlib import Path
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_DENIED = "Brak uprawnienia can_manage_inbound_messages na organization"
_ENDPOINTS = (
    ("GET", "/api/v1/inbound-messages", None, None),
    (
        "POST",
        "/api/v1/inbound-messages",
        None,
        {
            "source_ref": "fixture://inbound-mail/1",
            "from_address": "ops@carrier.example",
            "subject": "RFQ",
            "body_text": "treść",
        },
    ),
    (
        "POST",
        f"/api/v1/inbound-messages/{uuid4()}/resolve-email",
        None,
        None,
    ),
    (
        "POST",
        f"/api/v1/inbound-messages/{uuid4()}/extract",
        None,
        None,
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
def test_inbound_message_endpoints_are_forbidden_without_permission(
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


def test_authorization_model_grants_inbound_messages_to_organization_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_inbound_messages"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_inbound_messages_relation() -> None:
    source = (_ROOT / "authz" / "model.fga").read_text(encoding="utf-8")
    assert "can_manage_inbound_messages: member" in source
