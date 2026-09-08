from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_quotations na organization"
_ENDPOINTS = (
    (
        "GET",
        "/api/v1/document-checklist-rules",
        {"incoterm": "FOB", "trade_side": "export", "mode": "ocean"},
        None,
    ),
    (
        "POST",
        "/api/v1/document-checklist-rules",
        None,
        {
            "incoterm": "FOB",
            "trade_side": "export",
            "mode": "ocean",
            "document_kind": "bill_of_lading",
            "blocks_dispatch": True,
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
def _reset_authz() -> object:
    set_authz_checker(None)
    yield
    set_authz_checker(None)


@pytest.mark.parametrize(("method", "path", "params", "json_body"), _ENDPOINTS)
def test_checklist_endpoints_are_forbidden_without_permission(
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
