from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from app.core.database import bind_tenant
from app.models.carrier_profile import CarrierProfile
from app.models.channel_quote import ChannelQuote
from app.models.party import Party
from app.models.port import Port
from app.repositories.channel_quotes.channel_quote_repository import ChannelQuoteRepository

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
    amount: str,
    currency: str,
    transit_days: int | None,
) -> ChannelQuote:
    return ChannelQuote(
        id=uuid4(),
        organization_id=organization_id,
        amount=Decimal(amount),
        currency=currency,
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        quote_date=date(2026, 9, 1),
        transit_days=transit_days,
        source_ref=_MANUAL,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sql_badges_group_by_lane_day_and_currency(session, two_tenants) -> None:
    org = two_tenants["org_a"]
    user = two_tenants["user_a"]
    await bind_tenant(session, org.id)
    cheap = _party(organization_id=org.id, legal_name="Tani", created_by=user.id)
    fast = _party(organization_id=org.id, legal_name="Szybki", created_by=user.id)
    euro = _party(organization_id=org.id, legal_name="Euro", created_by=user.id)
    session.add_all([cheap, fast, euro])
    await session.flush()
    for party in (cheap, fast, euro):
        session.add(
            CarrierProfile(
                id=uuid4(),
                organization_id=org.id,
                party_id=party.id,
                is_nvocc=False,
                api_adapter="none",
            ),
        )
    origin = _port(organization_id=org.id, unlocode="CNSHA")
    dest = _port(organization_id=org.id, unlocode="NLRTM")
    session.add_all([origin, dest])
    await session.flush()
    cheap_row = _quote(
        organization_id=org.id,
        party_id=cheap.id,
        origin_port_id=origin.id,
        destination_port_id=dest.id,
        created_by=user.id,
        amount="800.0000",
        currency="USD",
        transit_days=None,
    )
    fast_row = _quote(
        organization_id=org.id,
        party_id=fast.id,
        origin_port_id=origin.id,
        destination_port_id=dest.id,
        created_by=user.id,
        amount="1200.0000",
        currency="USD",
        transit_days=18,
    )
    euro_row = _quote(
        organization_id=org.id,
        party_id=euro.id,
        origin_port_id=origin.id,
        destination_port_id=dest.id,
        created_by=user.id,
        amount="100.0000",
        currency="EUR",
        transit_days=30,
    )
    session.add_all([cheap_row, fast_row, euro_row])
    await session.flush()

    listed = await ChannelQuoteRepository(session).list_with_badges()
    cards = {card.quote.id: card for card in listed}
    assert cards[cheap_row.id].is_cheapest is True
    assert cards[cheap_row.id].is_fastest_tt is False
    assert cards[fast_row.id].is_cheapest is False
    assert cards[fast_row.id].is_fastest_tt is True
    assert cards[euro_row.id].is_cheapest is True
    assert cards[euro_row.id].is_fastest_tt is True
