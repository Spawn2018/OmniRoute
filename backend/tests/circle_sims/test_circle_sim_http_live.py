import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.deps import set_authz_checker
from app.core.database import bind_tenant, get_session
from app.main import app
from tests.circle_sims.test_circle_sim_isolation import _row
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
async def test_http_pairs_live_from_complementary_rows(
    live_client: AsyncClient, session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add_all(
        [
            _row(
                organization_id=org_a.id,
                created_by=user_a.id,
                sim_code="out_live",
                unload_unlocode="PLGDY",
                load_unlocode="DEHAM",
                source_ref="fixture://circle-sim/out-live",
            ),
            _row(
                organization_id=org_a.id,
                created_by=user_a.id,
                sim_code="back_live",
                unload_unlocode="DEHAM",
                load_unlocode="PLGDY",
                source_ref="fixture://circle-sim/back-live",
            ),
        ]
    )
    await session.commit()
    headers = bearer_auth_headers(organization_id=org_a.id, user_id=user_a.id)
    listed = await live_client.get("/api/v1/circle-sim-pairs", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    codes = {rows[0]["left_sim_code"], rows[0]["right_sim_code"]}
    assert codes == {"out_live", "back_live"}
    assert "amount" not in rows[0]
    assert "loaded_km" not in rows[0]
