from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_networks na organization"
_PATHS = (
    ("GET", "/api/v1/carrier-inquiries", None),
    ("POST", "/api/v1/carrier-inquiries", {"network_member_id": str(uuid4())}),
    (
        "POST",
        "/api/v1/carrier-inquiries/batch",
        {"network_member_ids": [str(uuid4())]},
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


@pytest.mark.parametrize(("method", "path", "payload"), _PATHS)
def test_carrier_inquiry_endpoints_need_networks_permission(
    method: str,
    path: str,
    payload: dict[str, object] | None,
) -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).request(
        method,
        path,
        headers=bearer_auth_headers(),
        json=payload,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED
