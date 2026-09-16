from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.domain.errors import InvalidCarrierInquiry, ResourceNotFound
from app.models.carrier_inquiry import CarrierInquiry
from app.models.network import Network
from app.models.network_member import NetworkMember
from app.services.carrier_inquiries.carrier_inquiry_service import CarrierInquiryService


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


def _answered(*, organization_id, user_id, member: NetworkMember) -> CarrierInquiry:
    return CarrierInquiry(
        id=uuid4(),
        organization_id=organization_id,
        network_member_id=member.id,
        source_ref="tenant:manual",
        status="answered",
        quoted_amount=Decimal("10.0000"),
        quoted_currency="USD",
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carrier_inquiry_ranking_orders_answered_then_zero(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    net_a = _network(organization_id=org_a.id, user_id=user_a.id, suffix="r")
    net_b = _network(organization_id=org_b.id, user_id=user_b.id, suffix="s")
    high = _member(organization_id=org_a.id, user_id=user_a.id, network=net_a, suffix="h")
    mid = _member(organization_id=org_a.id, user_id=user_a.id, network=net_a, suffix="m")
    zero = _member(organization_id=org_a.id, user_id=user_a.id, network=net_a, suffix="z")
    foreign = _member(organization_id=org_b.id, user_id=user_b.id, network=net_b, suffix="f")

    await bind_tenant(session, org_a.id)
    session.add(net_a)
    await session.flush()
    session.add_all([high, mid, zero])
    await session.flush()
    session.add_all(
        [
            _answered(organization_id=org_a.id, user_id=user_a.id, member=high),
            _answered(organization_id=org_a.id, user_id=user_a.id, member=high),
            _answered(organization_id=org_a.id, user_id=user_a.id, member=mid),
            _inquiry(organization_id=org_a.id, user_id=user_a.id, member=zero),
        ],
    )
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(net_b)
    await session.flush()
    session.add(foreign)
    await session.flush()
    session.add(_answered(organization_id=org_b.id, user_id=user_b.id, member=foreign))
    await session.flush()

    await bind_tenant(session, org_a.id)
    ranks = await CarrierInquiryService(session).list_member_ranks()
    assert [row.network_member_id for row in ranks] == [high.id, mid.id, zero.id]
    assert [row.answered_count for row in ranks] == [2, 1, 0]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carrier_inquiry_overdue_is_sql_current_date(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    net_a = _network(organization_id=org_a.id, user_id=user_a.id, suffix="d")
    member_a = _member(organization_id=org_a.id, user_id=user_a.id, network=net_a, suffix="d")
    past = _inquiry(organization_id=org_a.id, user_id=user_a.id, member=member_a)
    past.no_reply_after = date.today() - timedelta(days=1)
    blank = _inquiry(organization_id=org_a.id, user_id=user_a.id, member=member_a)

    await bind_tenant(session, org_a.id)
    session.add(net_a)
    await session.flush()
    session.add(member_a)
    await session.flush()
    session.add_all([past, blank])
    await session.flush()

    rows = await CarrierInquiryService(session).list_inquiries(silent="overdue")
    assert [row.id for row in rows] == [past.id]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_mark_answered_updates_sent_inquiry(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    net_a = _network(organization_id=org_a.id, user_id=user_a.id, suffix="m")
    member_a = _member(organization_id=org_a.id, user_id=user_a.id, network=net_a, suffix="m")
    inquiry = _inquiry(organization_id=org_a.id, user_id=user_a.id, member=member_a)
    inquiry.status = "sent"

    await bind_tenant(session, org_a.id)
    session.add(net_a)
    await session.flush()
    session.add(member_a)
    await session.flush()
    session.add(inquiry)
    await session.flush()

    updated = await CarrierInquiryService(session).mark_answered(
        inquiry_id=inquiry.id,
        quoted_amount="15.0000",
        quoted_currency="USD",
        quoted_transit_days=9,
    )
    assert updated.status == "answered"
    assert updated.quoted_amount == Decimal("15.0000")
    assert updated.quoted_currency == "USD"
    assert updated.quoted_transit_days == 9


@pytest.mark.integration
@pytest.mark.asyncio
async def test_mark_answered_rejects_already_answered(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    net_a = _network(organization_id=org_a.id, user_id=user_a.id, suffix="n")
    member_a = _member(organization_id=org_a.id, user_id=user_a.id, network=net_a, suffix="n")
    inquiry = _answered(organization_id=org_a.id, user_id=user_a.id, member=member_a)

    await bind_tenant(session, org_a.id)
    session.add(net_a)
    await session.flush()
    session.add(member_a)
    await session.flush()
    session.add(inquiry)
    await session.flush()

    with pytest.raises(InvalidCarrierInquiry, match="nie pozwala"):
        await CarrierInquiryService(session).mark_answered(
            inquiry_id=inquiry.id,
            quoted_amount="20.0000",
            quoted_currency="EUR",
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_mark_answered_isolates_foreign_inquiry(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_b = two_tenants["user_b"]
    net_b = _network(organization_id=org_b.id, user_id=user_b.id, suffix="f")
    member_b = _member(organization_id=org_b.id, user_id=user_b.id, network=net_b, suffix="f")
    inquiry_b = _inquiry(organization_id=org_b.id, user_id=user_b.id, member=member_b)
    inquiry_b.status = "queued"

    await bind_tenant(session, org_b.id)
    session.add(net_b)
    await session.flush()
    session.add(member_b)
    await session.flush()
    session.add(inquiry_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    with pytest.raises(ResourceNotFound, match="zapytanie"):
        await CarrierInquiryService(session).mark_answered(
            inquiry_id=inquiry_b.id,
            quoted_amount="10.0000",
            quoted_currency="USD",
        )
