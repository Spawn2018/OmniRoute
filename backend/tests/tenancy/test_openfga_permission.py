from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app


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
        headers={
            "X-Organization-Id": str(uuid4()),
            "X-User-Id": str(uuid4()),
        },
    )
    assert response.status_code == 403
