import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers


class DenyAllAuthz:
    async def check(self, *, user_id, relation, object_type, object_id) -> bool:
        return False


@pytest.fixture(autouse=True)
def _reset_authz():
    set_authz_checker(None)
    yield
    set_authz_checker(None)


def test_list_users_forbidden_without_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    client = TestClient(app)
    response = client.get(
        "/api/v1/tenancy/users",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 403
