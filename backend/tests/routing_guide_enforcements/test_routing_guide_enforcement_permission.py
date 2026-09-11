from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_routing_guide_enforcements na organization"


class DenyEnforcementAuthz:
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


def test_routing_guide_enforcement_endpoints_forbidden() -> None:
    set_authz_checker(DenyEnforcementAuthz())
    client = TestClient(app)
    listed = client.get(
        "/api/v1/routing-guide-enforcements", headers=bearer_auth_headers()
    )
    assert listed.status_code == 403
    assert listed.json()["detail"] == _DENIED


def test_authorization_model_grants_enforcement_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_routing_guide_enforcements"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_enforcement_relation() -> None:
    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(
        encoding="utf-8",
    )
    assert "can_manage_routing_guide_enforcements: member" in source
