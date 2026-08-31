from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.core.session_token import encode_session_token
from app.main import app
from tests.http_auth import bearer_auth_headers


class RecordingDenyAuthz:
    def __init__(self) -> None:
        self.object_ids: list[object] = []
        self.user_ids: list[object] = []

    async def check(self, *, user_id, relation, object_type, object_id) -> bool:
        self.user_ids.append(user_id)
        self.object_ids.append(object_id)
        return False


def test_session_me_rejects_missing_token() -> None:
    response = TestClient(app).get("/api/v1/session/me")
    assert response.status_code == 401


def test_session_me_rejects_invalid_token() -> None:
    response = TestClient(app).get(
        "/api/v1/session/me",
        headers={"Authorization": "Bearer not-a-jwt"},
    )
    assert response.status_code == 401


def test_session_me_ignores_spoofed_tenant_headers() -> None:
    org_a = uuid4()
    user_a = uuid4()
    token = encode_session_token(user_id=user_a, organization_id=org_a)
    response = TestClient(app).get(
        "/api/v1/session/me",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Organization-Id": str(uuid4()),
            "X-User-Id": str(uuid4()),
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["organization_id"] == str(org_a)
    assert body["user_id"] == str(user_a)


def test_protected_route_rejects_missing_token() -> None:
    response = TestClient(app).get("/api/v1/tenancy/users")
    assert response.status_code == 401


def test_spoofed_organization_header_does_not_change_authz_tenant() -> None:
    async def _fake_tenant_session() -> object:
        return object()

    org_a = uuid4()
    user_a = uuid4()
    recorder = RecordingDenyAuthz()
    set_authz_checker(recorder)
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    try:
        response = TestClient(app).get(
            "/api/v1/tenancy/users",
            headers={
                **bearer_auth_headers(organization_id=org_a, user_id=user_a),
                "X-Organization-Id": str(uuid4()),
                "X-User-Id": str(uuid4()),
            },
        )
    finally:
        app.dependency_overrides.clear()
        set_authz_checker(None)
    assert response.status_code == 403
    assert recorder.object_ids == [org_a]
    assert recorder.user_ids == [user_a]


def test_session_token_requires_body() -> None:
    response = TestClient(app).post("/api/v1/session/token", json={})
    assert response.status_code == 422
