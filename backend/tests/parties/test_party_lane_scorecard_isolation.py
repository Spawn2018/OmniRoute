from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.party_lane_scorecard import PartyLaneScorecard
from app.models.port import Port

_MANUAL = "tenant:manual"
_UNLOCODE_SOURCE = "github:cristan/improved-un-locodes@fixture"


def _party(*, organization_id, legal_name: str, created_by):
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["agent"],
        source_ref=_MANUAL,
        is_active=True,
        created_by=created_by,
    )


def _port(*, organization_id, unlocode: str) -> Port:
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


def _card(*, organization_id, user_id, party, origin, dest) -> PartyLaneScorecard:
    return PartyLaneScorecard(
        id=uuid4(),
        organization_id=organization_id,
        party_id=party.id,
        origin_port_id=origin.id,
        destination_port_id=dest.id,
        window_days=90,
        sample_size=0,
        answered_inquiry_count=0,
        shipment_count=0,
        cheapest_count=0,
        source_ref=_MANUAL,
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_lane_scorecard_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Agent A", created_by=user_a.id)
    origin_a = _port(organization_id=org_a.id, unlocode="CNSHA")
    dest_a = _port(organization_id=org_a.id, unlocode="NLRTM")
    session.add_all([party_a, origin_a, dest_a])
    await session.flush()
    card_a = _card(
        organization_id=org_a.id,
        user_id=user_a.id,
        party=party_a,
        origin=origin_a,
        dest=dest_a,
    )
    session.add(card_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Agent B", created_by=user_b.id)
    origin_b = _port(organization_id=org_b.id, unlocode="CNSHA")
    dest_b = _port(organization_id=org_b.id, unlocode="NLRTM")
    session.add_all([party_b, origin_b, dest_b])
    await session.flush()
    card_b = _card(
        organization_id=org_b.id,
        user_id=user_b.id,
        party=party_b,
        origin=origin_b,
        dest=dest_b,
    )
    session.add(card_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PartyLaneScorecard))).all())
    assert {row.id for row in visible_a} == {card_a.id}
    assert (
        await session.scalar(select(PartyLaneScorecard).where(PartyLaneScorecard.id == card_b.id))
        is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PartyLaneScorecard))).all())
    assert {row.id for row in visible_b} == {card_b.id}
    assert (
        await session.scalar(select(PartyLaneScorecard).where(PartyLaneScorecard.id == card_a.id))
        is None
    )
