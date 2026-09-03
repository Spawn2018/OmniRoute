from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.edi_message import EdiMessage
from app.models.party import Party
from app.models.quotation import Quotation
from app.models.rate_line import RateLine
from app.models.shipment import Shipment

_MANUAL = "tenant:manual"


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


def _party(*, organization_id, legal_name: str, created_by) -> Party:
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["customer"],
        source_ref=_MANUAL,
        is_active=True,
        created_by=created_by,
    )


async def _booked(session, *, organization_id, user_id, suffix: str) -> Shipment:
    rate = _buy_rate(
        organization_id=organization_id,
        created_by=user_id,
        source_ref=f"tariff://{suffix}",
    )
    party = _party(
        organization_id=organization_id,
        legal_name=f"Klient {suffix}",
        created_by=user_id,
    )
    session.add_all([rate, party])
    await session.flush()
    quote = _quote(
        organization_id=organization_id,
        created_by=user_id,
        rate_line_id=rate.id,
        source_ref=f"tariff://{suffix}",
    )
    session.add(quote)
    await session.flush()
    ship = Shipment(
        id=uuid4(),
        organization_id=organization_id,
        quotation_id=quote.id,
        party_id=party.id,
        source_ref=f"fixture://shipment/{suffix}",
        status="draft",
        created_by=user_id,
    )
    session.add(ship)
    await session.flush()
    return ship


@pytest.mark.integration
@pytest.mark.asyncio
async def test_edi_message_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="a")
    row_a = EdiMessage(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        message_kind="noted",
        source_ref="fixture://edi-message/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="b")
    row_b = EdiMessage(
        id=uuid4(),
        organization_id=org_b.id,
        shipment_id=ship_b.id,
        message_kind="outbound",
        source_ref="fixture://edi-message/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(EdiMessage))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    foreign_b = await session.scalar(select(EdiMessage).where(EdiMessage.id == row_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(EdiMessage))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_edi_message_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="b")

    await bind_tenant(session, org_a.id)
    stolen = EdiMessage(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_b.id,
        message_kind="other",
        source_ref="fixture://edi-message/stolen",
        created_by=user_a.id,
    )
    session.add(stolen)
    with pytest.raises(IntegrityError):
        await session.flush()
