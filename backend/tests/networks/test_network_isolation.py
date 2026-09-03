from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.network import Network
from app.models.network_member import NetworkMember


@pytest.mark.integration
@pytest.mark.asyncio
async def test_network_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    net_a = Network(
        id=uuid4(),
        organization_id=org_a.id,
        code="wca",
        name="WCA A",
        aliases=["wca_a"],
        source_ref="tenant:manual",
        created_by=user_a.id,
    )
    net_b = Network(
        id=uuid4(),
        organization_id=org_b.id,
        code="wca",
        name="WCA B",
        aliases=["wca_b"],
        source_ref="tenant:manual",
        created_by=user_b.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(net_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(net_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Network))).all())
    assert {row.id for row in visible_a} == {net_a.id}
    foreign_b = await session.scalar(select(Network).where(Network.id == net_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Network))).all())
    assert {row.id for row in visible_b} == {net_b.id}
    foreign_a = await session.scalar(select(Network).where(Network.id == net_a.id))
    assert foreign_a is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_network_member_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    net_a = Network(
        id=uuid4(),
        organization_id=org_a.id,
        code="wca",
        name="WCA A",
        aliases=[],
        source_ref="tenant:manual",
        created_by=user_a.id,
    )
    net_b = Network(
        id=uuid4(),
        organization_id=org_b.id,
        code="wca",
        name="WCA B",
        aliases=[],
        source_ref="tenant:manual",
        created_by=user_b.id,
    )
    member_a = NetworkMember(
        id=uuid4(),
        organization_id=org_a.id,
        network_id=net_a.id,
        member_code="agent_a",
        legal_name="Agent A",
        source_ref="tenant:manual",
        created_by=user_a.id,
    )
    member_b = NetworkMember(
        id=uuid4(),
        organization_id=org_b.id,
        network_id=net_b.id,
        member_code="agent_b",
        legal_name="Agent B",
        source_ref="tenant:manual",
        created_by=user_b.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(net_a)
    await session.flush()
    session.add(member_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(net_b)
    await session.flush()
    session.add(member_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(NetworkMember))).all())
    assert {row.id for row in visible_a} == {member_a.id}
    foreign_b = await session.scalar(select(NetworkMember).where(NetworkMember.id == member_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(NetworkMember))).all())
    assert {row.id for row in visible_b} == {member_b.id}
