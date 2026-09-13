from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.deps import set_authz_checker
from app.core.database import bind_tenant, get_session
from app.main import app
from app.models.plan_snapshot import PlanSnapshot
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


async def _seed_snapshot(session, *, organization_id, created_by, suffix: str):
    ship, trip, res = await _triple(
        session, organization_id=organization_id, created_by=created_by, suffix=suffix
    )
    row = PlanSnapshot(
        id=uuid4(),
        organization_id=organization_id,
        snapshot_code=f"plan_{suffix}"[:32],
        shipment_id=ship,
        trip_id=trip,
        resource_id=res,
        author_label="Anna",
        recorded_at=datetime(2026, 9, 10, 12, 0, tzinfo=UTC),
        source_ref=f"fixture://plan-snapshot/{suffix}",
        created_by=created_by,
    )
    session.add(row)
    await session.flush()
    return row


def _run_body(*, plan_snapshot_id, code: str, origin: str) -> dict[str, str]:
    return {
        "run_code": code,
        "plan_snapshot_id": str(plan_snapshot_id),
        "baseline_label": "plan z wczoraj",
        "levers_label": "paliwo w gore",
        "result_label": "eta plus dwie godziny",
        "source_ref": origin,
    }


@pytest.mark.integration
@pytest.mark.asyncio
async def test_http_create_live_requires_existing_snapshot(
    live_client: AsyncClient, session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    snap = await _seed_snapshot(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="cflive"
    )
    await session.commit()
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    created = await live_client.post(
        "/api/v1/counterfactual-runs",
        headers=headers,
        json=_run_body(
            plan_snapshot_id=snap.id,
            code="fuel_spike",
            origin="fixture://counterfactual-run/live",
        ),
    )
    assert created.status_code == 201
    assert created.json()["plan_snapshot_id"] == str(snap.id)
    missing = await live_client.post(
        "/api/v1/counterfactual-runs",
        headers=headers,
        json=_run_body(
            plan_snapshot_id=uuid4(),
            code="port_close",
            origin="fixture://counterfactual-run/missing",
        ),
    )
    assert missing.status_code == 400
    assert "migawka" in missing.json()["detail"]
    replay = await live_client.get("/api/v1/what-if-replays", headers=headers)
    assert replay.status_code == 200
    rows = replay.json()
    assert len(rows) == 1
    assert rows[0]["snapshot_code"] == "plan_cflive"
    assert rows[0]["run_code"] == "fuel_spike"
