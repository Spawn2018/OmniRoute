from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_collaboration_marks na organization"


class DenyCollabAuthz:
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


def test_collaboration_endpoints_forbidden() -> None:
    set_authz_checker(DenyCollabAuthz())
    client = TestClient(app)
    listed = client.get(
        "/api/v1/collaboration-marks", headers=bearer_auth_headers()
    )
    assert listed.status_code == 403
    assert listed.json()["detail"] == _DENIED


def test_authorization_model_grants_collaboration_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_collaboration_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_collaboration_relation() -> None:
    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(
        encoding="utf-8",
    )
    assert "can_manage_collaboration_marks: member" in source
