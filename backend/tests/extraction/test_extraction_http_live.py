from base64 import b64encode

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.deps import set_authz_checker
from app.core.database import get_session
from app.main import app
from tests.extraction.test_xlsx_sheet import _xlsx_bytes
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(self, *, user_id, relation, object_type, object_id) -> bool:
        return True


@pytest_asyncio.fixture
async def live_client(engine) -> AsyncClient:
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async def _override_session():
        async with factory() as session:
            yield session

    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[get_session] = _override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
    set_authz_checker(None)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_extract_live_pg_creates_pending_draft(
    live_client: AsyncClient, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    response = await live_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
        json={"source_ref": "doc://live", "input_text": "THC 10 EUR"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["organization_id"] == str(org_a.id)
    assert "rate_line" not in body["payload"]
    assert body["payload"]["extract_path"] == "text"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_token_a_cannot_accept_draft_b(
    live_client: AsyncClient, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    created = await live_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_b.id, user_id=user_b.id),
        json={"source_ref": "doc://b", "input_text": "THC 10 EUR"},
    )
    assert created.status_code == 201
    draft_b = created.json()["id"]
    stolen = await live_client.post(
        f"/api/v1/extractions/{draft_b}/accept",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
    )
    assert stolen.status_code == 404
    listed = await live_client.get(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
    )
    assert listed.status_code == 200
    assert listed.json() == []
    rates = await live_client.get(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
    )
    assert rates.status_code == 200
    assert rates.json() == []


async def _seed_thc(live_client: AsyncClient, *, org_id, user_id) -> None:
    created = await live_client.post(
        "/api/v1/charge-codes",
        headers=bearer_auth_headers(organization_id=org_id, user_id=user_id),
        json={"code": "THC", "name": "Terminal handling", "aliases": []},
    )
    assert created.status_code == 201


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_accept_writes_rate_line_same_transaction(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    await _seed_thc(live_client, org_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://live-accept", "input_text": "THC 10 EUR"},
    )
    assert created.status_code == 201
    draft_id = created.json()["id"]
    accepted = await live_client.post(f"/api/v1/extractions/{draft_id}/accept", headers=headers)
    assert accepted.status_code == 200
    body = accepted.json()
    assert body["status"] == "accepted"
    assert len(body["rate_line_ids"]) == 1
    rates = await live_client.get("/api/v1/rate-lines", headers=headers)
    assert rates.status_code == 200
    rows = rates.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["rate_line_ids"][0]
    assert rows[0]["charge_code"] == "THC"
    assert rows[0]["source_ref"] == "doc://live-accept"
    assert rows[0]["amount"] == "10.0000"
    assert rows[0]["currency"] == "EUR"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_accept_unknown_code_rolls_back_draft(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://no-catalog", "input_text": "THC 10 EUR"},
    )
    assert created.status_code == 201
    draft_id = created.json()["id"]
    accepted = await live_client.post(f"/api/v1/extractions/{draft_id}/accept", headers=headers)
    assert accepted.status_code == 400
    assert "nieznany kod opłaty" in accepted.json()["detail"]
    pending = await live_client.get("/api/v1/extractions", headers=headers)
    assert pending.status_code == 200
    rows = pending.json()
    assert len(rows) == 1
    assert rows[0]["id"] == draft_id
    assert rows[0]["status"] == "pending"
    rates = await live_client.get("/api/v1/rate-lines", headers=headers)
    assert rates.status_code == 200
    assert rates.json() == []


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_token_a_cannot_create_rate_for_draft_b(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    headers_b = bearer_auth_headers(organization_id=org_b.id, user_id=user_b.id)
    await _seed_thc(live_client, org_id=org_b.id, user_id=user_b.id)
    created = await live_client.post(
        "/api/v1/extractions",
        headers=headers_b,
        json={"source_ref": "doc://b-rate", "input_text": "THC 10 EUR"},
    )
    assert created.status_code == 201
    draft_b = created.json()["id"]
    stolen = await live_client.post(
        f"/api/v1/extractions/{draft_b}/accept",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
    )
    assert stolen.status_code == 404
    rates_a = await live_client.get(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
    )
    rates_b = await live_client.get("/api/v1/rate-lines", headers=headers_b)
    assert rates_a.status_code == 200
    assert rates_a.json() == []
    assert rates_b.status_code == 200
    assert rates_b.json() == []
    pending_b = await live_client.get("/api/v1/extractions", headers=headers_b)
    assert pending_b.status_code == 200
    assert pending_b.json()[0]["status"] == "pending"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_patch_live_replaces_candidates_without_rate_line(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://patch", "input_text": "THC 10 EUR"},
    )
    assert created.status_code == 201
    draft_id = created.json()["id"]
    patched = await live_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={
            "candidates": [
                {"code": "BAF", "amount_text": "12", "currency": "USD", "note": "HITL"},
            ],
        },
    )
    assert patched.status_code == 200
    assert patched.json()["payload"]["candidates"][0]["code"] == "BAF"
    assert patched.json()["payload"]["source_ref"] == "doc://patch"
    listed = await live_client.get("/api/v1/extractions", headers=headers)
    assert listed.json()[0]["payload"]["candidates"][0]["amount_text"] == "12"
    assert created.json()["payload"]["revision"] == 0
    assert patched.json()["payload"]["revision"] == 1
    rates = await live_client.get("/api/v1/rate-lines", headers=headers)
    assert rates.status_code == 200
    assert rates.json() == []


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_token_a_cannot_patch_draft_b(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    created = await live_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_b.id, user_id=user_b.id),
        json={"source_ref": "doc://b-patch", "input_text": "THC 10 EUR"},
    )
    assert created.status_code == 201
    draft_b = created.json()["id"]
    stolen = await live_client.patch(
        f"/api/v1/extractions/{draft_b}",
        headers=bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id),
        json={"candidates": [{"code": "THC", "amount_text": "99", "currency": "EUR"}]},
    )
    assert stolen.status_code == 404
    listed_b = await live_client.get(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_b.id, user_id=user_b.id),
    )
    assert listed_b.json()[0]["payload"]["candidates"][0]["amount_text"] == "10"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_patch_after_accept_returns_409(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    await _seed_thc(live_client, org_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://after-accept", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    accepted = await live_client.post(f"/api/v1/extractions/{draft_id}/accept", headers=headers)
    assert accepted.status_code == 200
    patched = await live_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={"candidates": [{"code": "THC", "amount_text": "11", "currency": "EUR"}]},
    )
    assert patched.status_code == 409


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_extract_live_image_path_does_not_write_rate_line(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={
            "source_ref": "doc://image-label",
            "input_text": "THC 10 EUR",
            "extract_path": "image",
        },
    )
    assert created.status_code == 201
    assert created.json()["payload"]["extract_path"] == "image"
    listed = await live_client.get("/api/v1/extractions", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["payload"]["extract_path"] == "image"
    rates = await live_client.get("/api/v1/rate-lines", headers=headers)
    assert rates.status_code == 200
    assert rates.json() == []


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_extract_live_xlsx_creates_pending_draft(
    live_client: AsyncClient,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={
            "source_ref": "doc://xlsx",
            "document_base64": b64encode(_xlsx_bytes()).decode("ascii"),
        },
    )
    assert created.status_code == 201
    assert created.json()["payload"]["parser_name"] == "xlsx_sheet"
    assert created.json()["payload"]["candidates"][0]["code"] == "THC"
    rates = await live_client.get("/api/v1/rate-lines", headers=headers)
    assert rates.status_code == 200
    assert rates.json() == []
