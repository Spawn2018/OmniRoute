from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.party_scorecard import PartyScorecard

_MANUAL = "tenant:manual"


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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_scorecard_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Agent A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    card_a = PartyScorecard(
        id=uuid4(),
        organization_id=org_a.id,
        party_id=party_a.id,
        window_days=90,
        sample_size=3,
        response_rate=Decimal("0.8000"),
        source_ref=_MANUAL,
        created_by=user_a.id,
    )
    session.add(card_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Agent B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    card_b = PartyScorecard(
        id=uuid4(),
        organization_id=org_b.id,
        party_id=party_b.id,
        window_days=90,
        sample_size=3,
        response_rate=Decimal("0.8000"),
        source_ref=_MANUAL,
        created_by=user_b.id,
    )
    session.add(card_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PartyScorecard))).all())
    assert {row.id for row in visible_a} == {card_a.id}
    assert (
        await session.scalar(select(PartyScorecard).where(PartyScorecard.id == card_b.id)) is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PartyScorecard))).all())
    assert {row.id for row in visible_b} == {card_b.id}
    assert (
        await session.scalar(select(PartyScorecard).where(PartyScorecard.id == card_a.id)) is None
    )
