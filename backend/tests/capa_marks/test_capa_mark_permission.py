from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_capa_marks na organization"
_CALLS = (
    ("GET", "/api/v1/capa-marks", None, None),
    (
        "POST",
        "/api/v1/capa-marks",
        None,
        {
            "mark_code": "capa_pl_01",
            "mark_kind": "capa",
            "source_ref": "fixture://capa-mark/pl-1",
        },
    ),
)


class DenyCapaMarkAuthz:
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


@pytest.mark.parametrize(("method", "path", "params", "json_body"), _CALLS)
def test_capa_mark_endpoints_are_forbidden_without_permission(
    method: str,
    path: str,
    params: dict[str, str] | None,
    json_body: dict[str, object] | None,
) -> None:
    set_authz_checker(DenyCapaMarkAuthz())
    response = TestClient(app).request(
        method,
        path,
        headers=bearer_auth_headers(),
        params=params,
        json=json_body,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_authorization_model_grants_capa_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_capa_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_capa_mark_relation() -> None:
    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(
        encoding="utf-8",
    )
    assert "can_manage_capa_marks: member" in source
