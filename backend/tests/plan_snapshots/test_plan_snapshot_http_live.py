from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.deps import set_authz_checker
from app.core.database import bind_tenant, get_session
from app.main import app
from tests.http_auth import bearer_auth_headers
from tests.plan_snapshots.test_plan_snapshot_isolation import _triple


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


def _body(*, shipment_id, trip_id, resource_id, code: str, origin: str) -> dict[str, str]:
    return {
        "snapshot_code": code,
        "shipment_id": str(shipment_id),
        "trip_id": str(trip_id),
        "resource_id": str(resource_id),
        "author_label": "Anna",
        "recorded_at": "2026-09-10T12:00:00+02:00",
        "source_ref": origin,
    }


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_create_live_requires_existing_triple(
    live_client: AsyncClient, session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship, trip, res = await _triple(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="live"
    )
    await session.commit()
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/plan-snapshots",
        headers=headers,
        json=_body(
            shipment_id=ship,
            trip_id=trip,
            resource_id=res,
            code="plan_v1",
            origin="fixture://plan-snapshot/live",
        ),
    )
    assert created.status_code == 201
    assert created.json()["snapshot_code"] == "plan_v1"
    missing = await live_client.post(
        "/api/v1/plan-snapshots",
        headers=headers,
        json=_body(
            shipment_id=uuid4(),
            trip_id=trip,
            resource_id=res,
            code="plan_v2",
            origin="fixture://plan-snapshot/missing",
        ),
    )
    assert missing.status_code == 400
    assert "trójka" in missing.json()["detail"]
