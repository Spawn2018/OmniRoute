from uuid import UUID, uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.port import Port


def _port(*, organization_id: UUID, unlocode: str, name: str, created_by: UUID) -> Port:
    return Port(
        id=uuid4(),
        organization_id=organization_id,
        unlocode=unlocode,
        name=name,
        country_code=unlocode[:2],
        is_seaport=True,
        function_flags=["port"],
        aliases=[],
        is_official=True,
        source_ref="github:cristan/improved-un-locodes@fixture",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_port_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    port_a = _port(
        organization_id=org_a.id,
        unlocode="PLGDY",
        name="Gdynia",
        created_by=two_tenants["user_a"].id,
    )
    port_b = _port(
        organization_id=org_b.id,
        unlocode="DEHAM",
        name="Hamburg",
        created_by=two_tenants["user_b"].id,
    )

    await bind_tenant(session, org_a.id)
    session.add(port_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(port_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Port))).all())
    assert {row.id for row in visible_a} == {port_a.id}
    assert await session.scalar(select(Port).where(Port.id == port_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Port))).all())
    assert {row.id for row in visible_b} == {port_b.id}
    assert await session.scalar(select(Port).where(Port.id == port_a.id)) is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_two_tenants_may_hold_the_same_unlocode(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    await bind_tenant(session, org_a.id)
    session.add(
        _port(
            organization_id=org_a.id,
            unlocode="PLGDY",
            name="Gdynia",
            created_by=two_tenants["user_a"].id,
        )
    )
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(
        _port(
            organization_id=org_b.id,
            unlocode="PLGDY",
            name="Gdynia",
            created_by=two_tenants["user_b"].id,
        )
    )
    await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_unlocode_is_unique_inside_one_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]

    await bind_tenant(session, org_a.id)
    session.add(
        _port(
            organization_id=org_a.id,
            unlocode="PLGDY",
            name="Gdynia",
            created_by=user_a.id,
        )
    )
    await session.flush()

    session.add(
        _port(
            organization_id=org_a.id,
            unlocode="PLGDY",
            name="Gdynia duplikat",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_port_without_tenant_context_is_invisible(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    session.add(
        _port(
            organization_id=org_a.id,
            unlocode="PLGDY",
            name="Gdynia",
            created_by=two_tenants["user_a"].id,
        )
    )
    await session.flush()
    session.expunge_all()

    await session.execute(text("SELECT set_config('app.current_org', '', true)"))
    assert list((await session.scalars(select(Port))).all()) == []
