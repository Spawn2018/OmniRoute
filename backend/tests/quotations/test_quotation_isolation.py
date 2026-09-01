from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.port import Port
from app.models.quotation import Quotation
from app.models.rate_line import RateLine

_UNLOCODE_SOURCE = "github:cristan/improved-un-locodes@fixture"


def _buy_rate(*, organization_id, created_by, source_ref: str) -> RateLine:
    return RateLine(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


def _quote(*, organization_id, created_by, rate_line_id, source_ref: str) -> Quotation:
    return Quotation(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        rate_line_id=rate_line_id,
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    session.add(rate_a)
    await session.flush()
    quote_a = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a",
    )
    session.add(quote_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")
    session.add(rate_b)
    await session.flush()
    quote_b = _quote(
        organization_id=org_b.id,
        created_by=user_b.id,
        rate_line_id=rate_b.id,
        source_ref="tariff://b",
    )
    session.add(quote_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Quotation))).all())
    assert {row.id for row in visible_a} == {quote_a.id}
    foreign_b = await session.scalar(select(Quotation).where(Quotation.id == quote_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Quotation))).all())
    assert {row.id for row in visible_b} == {quote_b.id}
    foreign_a = await session.scalar(select(Quotation).where(Quotation.id == quote_a.id))
    assert foreign_a is None


def _port(*, organization_id: UUID, unlocode: str) -> Port:
    return Port(
        id=uuid4(),
        organization_id=organization_id,
        unlocode=unlocode,
        name=unlocode,
        country_code=unlocode[:2],
        is_seaport=True,
        function_flags=["port"],
        aliases=[],
        is_official=True,
        source_ref=_UNLOCODE_SOURCE,
    )


def _party(*, organization_id: UUID, legal_name: str, created_by: UUID) -> Party:
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["customer"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=created_by,
    )


async def _lane(session, organization_id: UUID, created_by: UUID, unlocode_a: str, unlocode_b: str):
    origin = _port(organization_id=organization_id, unlocode=unlocode_a)
    destination = _port(organization_id=organization_id, unlocode=unlocode_b)
    party = _party(organization_id=organization_id, legal_name=unlocode_a, created_by=created_by)
    session.add_all([origin, destination, party])
    await session.flush()
    return origin, destination, party


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_may_not_point_party_at_another_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="ACME A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    origin, destination, _own_party = await _lane(session, org_b.id, user_b.id, "DEHAM", "NLRTM")
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")
    session.add(rate_b)
    await session.flush()
    session.add(
        Quotation(
            id=uuid4(),
            organization_id=org_b.id,
            charge_code="THC",
            rate_line_id=rate_b.id,
            amount=Decimal("10.0000"),
            currency="EUR",
            source_ref="tariff://b",
            created_by=user_b.id,
            origin_port_id=origin.id,
            destination_port_id=destination.id,
            party_id=party_a.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_quotation_party"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_may_not_point_origin_port_at_another_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    port_a = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    _origin, destination, party = await _lane(session, org_b.id, user_b.id, "DEHAM", "NLRTM")
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")
    session.add(rate_b)
    await session.flush()
    session.add(
        Quotation(
            id=uuid4(),
            organization_id=org_b.id,
            charge_code="THC",
            rate_line_id=rate_b.id,
            amount=Decimal("10.0000"),
            currency="EUR",
            source_ref="tariff://b",
            created_by=user_b.id,
            origin_port_id=port_a.id,
            destination_port_id=destination.id,
            party_id=party.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_quotation_origin_port"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_rejects_partial_lane_party_snapshot(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    origin, destination, _party_row = await _lane(session, org_a.id, user_a.id, "PLGDY", "DEHAM")
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    session.add(rate_a)
    await session.flush()
    session.add(
        Quotation(
            id=uuid4(),
            organization_id=org_a.id,
            charge_code="THC",
            rate_line_id=rate_a.id,
            amount=Decimal("10.0000"),
            currency="EUR",
            source_ref="tariff://a",
            created_by=user_a.id,
            origin_port_id=origin.id,
            destination_port_id=destination.id,
            party_id=None,
        )
    )
    with pytest.raises(IntegrityError, match="ck_quotation_lane_party_complete"):
        await session.flush()
