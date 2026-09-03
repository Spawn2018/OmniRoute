from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.carrier_inquiry import CarrierInquiry
from app.models.network import Network
from app.models.network_member import NetworkMember


def _network(*, organization_id, user_id, suffix: str) -> Network:
    return Network(
        id=uuid4(),
        organization_id=organization_id,
        code=f"wca{suffix}",
        name=f"Sieć {suffix}",
        aliases=[],
        source_ref="tenant:manual",
        created_by=user_id,
    )


def _member(*, organization_id, user_id, network: Network, suffix: str) -> NetworkMember:
    return NetworkMember(
        id=uuid4(),
        organization_id=organization_id,
        network_id=network.id,
        member_code=f"agent_{suffix}",
        legal_name=f"Agent {suffix}",
        source_ref="tenant:manual",
        created_by=user_id,
    )


def _inquiry(*, organization_id, user_id, member: NetworkMember) -> CarrierInquiry:
    return CarrierInquiry(
        id=uuid4(),
        organization_id=organization_id,
        network_member_id=member.id,
        source_ref="tenant:manual",
        status="draft",
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carrier_inquiry_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    net_a = _network(organization_id=org_a.id, user_id=user_a.id, suffix="a")
    net_b = _network(organization_id=org_b.id, user_id=user_b.id, suffix="b")
    member_a = _member(organization_id=org_a.id, user_id=user_a.id, network=net_a, suffix="a")
    member_b = _member(organization_id=org_b.id, user_id=user_b.id, network=net_b, suffix="b")
    inquiry_a = _inquiry(organization_id=org_a.id, user_id=user_a.id, member=member_a)
    inquiry_b = _inquiry(organization_id=org_b.id, user_id=user_b.id, member=member_b)

    await bind_tenant(session, org_a.id)
    session.add(net_a)
    await session.flush()
    session.add(member_a)
    await session.flush()
    session.add(inquiry_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(net_b)
    await session.flush()
    session.add(member_b)
    await session.flush()
    session.add(inquiry_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    seen_a = list((await session.scalars(select(CarrierInquiry))).all())
    assert {row.id for row in seen_a} == {inquiry_a.id}
    hidden = await session.scalar(
        select(CarrierInquiry).where(CarrierInquiry.id == inquiry_b.id),
    )
    assert hidden is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    seen_b = list((await session.scalars(select(CarrierInquiry))).all())
    assert {row.id for row in seen_b} == {inquiry_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carrier_inquiry_rejects_foreign_network_member(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    net_b = _network(organization_id=org_b.id, user_id=user_b.id, suffix="x")
    member_b = _member(organization_id=org_b.id, user_id=user_b.id, network=net_b, suffix="x")

    await bind_tenant(session, org_b.id)
    session.add(net_b)
    await session.flush()
    session.add(member_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        CarrierInquiry(
            id=uuid4(),
            organization_id=org_a.id,
            network_member_id=member_b.id,
            source_ref="tenant:manual",
            status="draft",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_carrier_inquiry_network_member"):
        await session.flush()
