from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.carrier_profile import CarrierProfile
from app.models.channel_quote import ChannelQuote
from app.models.party import Party
from app.models.port import Port

_UNLOCODE_SOURCE = "github:cristan/improved-un-locodes@fixture"
_MANUAL = "tenant:manual"


def _party(*, organization_id: UUID, legal_name: str, created_by: UUID) -> Party:
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["carrier"],
        source_ref=_MANUAL,
        is_active=True,
        created_by=created_by,
    )


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


def _quote(
    *,
    organization_id: UUID,
    party_id: UUID,
    origin_port_id: UUID,
    destination_port_id: UUID,
    created_by: UUID,
) -> ChannelQuote:
    return ChannelQuote(
        id=uuid4(),
        organization_id=organization_id,
        amount=Decimal("1200.0000"),
        currency="USD",
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        quote_date=date(2026, 9, 1),
        source_ref=_MANUAL,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_channel_quote_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Armator A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    session.add(
        CarrierProfile(
            id=uuid4(),
            organization_id=org_a.id,
            party_id=party_a.id,
            is_nvocc=False,
            api_adapter="none",
        ),
    )
    origin_a = _port(organization_id=org_a.id, unlocode="PLGDY")
    dest_a = _port(organization_id=org_a.id, unlocode="DEHAM")
    session.add_all([origin_a, dest_a])
    await session.flush()
    quote_a = _quote(
        organization_id=org_a.id,
        party_id=party_a.id,
        origin_port_id=origin_a.id,
        destination_port_id=dest_a.id,
        created_by=user_a.id,
    )
    session.add(quote_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Armator B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    session.add(
        CarrierProfile(
            id=uuid4(),
            organization_id=org_b.id,
            party_id=party_b.id,
            is_nvocc=False,
            api_adapter="maersk",
        ),
    )
    origin_b = _port(organization_id=org_b.id, unlocode="NLRTM")
    dest_b = _port(organization_id=org_b.id, unlocode="USNYC")
    session.add_all([origin_b, dest_b])
    await session.flush()
    quote_b = _quote(
        organization_id=org_b.id,
        party_id=party_b.id,
        origin_port_id=origin_b.id,
        destination_port_id=dest_b.id,
        created_by=user_b.id,
    )
    session.add(quote_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ChannelQuote))).all())
    assert {row.id for row in visible_a} == {quote_a.id}
    assert await session.scalar(select(ChannelQuote).where(ChannelQuote.id == quote_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ChannelQuote))).all())
    assert {row.id for row in visible_b} == {quote_b.id}
    assert await session.scalar(select(ChannelQuote).where(ChannelQuote.id == quote_a.id)) is None
