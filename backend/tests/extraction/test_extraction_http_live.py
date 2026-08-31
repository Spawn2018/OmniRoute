import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.deps import set_authz_checker
from app.core.database import get_session
from app.main import app
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(self, *, user_id, relation, object_type, object_id) -> bool:
        return True


@pytest.fixture
def live_client(engine):
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async def _override_session():
        async with factory() as session:
            yield session

    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[get_session] = _override_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


@pytest.mark.integration
def test_http_extract_live_pg_creates_pending_draft(live_client: TestClient, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    response = live_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
        json={"source_ref": "doc://live", "input_text": "THC 10 EUR"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["organization_id"] == str(org_a.id)
    assert "rate_line" not in body["payload"]


@pytest.mark.integration
def test_http_token_a_cannot_accept_draft_b(live_client: TestClient, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    created = live_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_b.id, user_id=user_b.id),
        json={"source_ref": "doc://b", "input_text": "THC 10 EUR"},
    )
    assert created.status_code == 201
    draft_b = created.json()["id"]
    stolen = live_client.post(
        f"/api/v1/extractions/{draft_b}/accept",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
    )
    assert stolen.status_code == 404
    listed = live_client.get(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
    )
    assert listed.status_code == 200
    assert listed.json() == []
