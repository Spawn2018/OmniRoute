from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
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


def _shipment(
    *,
    organization_id,
    user_id,
    quotation: Quotation,
    party: Party,
    shipment_ref: str | None = None,
) -> Shipment:
    return Shipment(
        id=uuid4(),
        organization_id=organization_id,
        quotation_id=quotation.id,
        party_id=party.id,
        source_ref="fixture://shipment/iso",
        shipment_ref=shipment_ref,
        status="draft",
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add_all([rate_a, party_a])
    await session.flush()
    quote_a = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a",
    )
    session.add(quote_a)
    await session.flush()
    ship_a = _shipment(
        organization_id=org_a.id,
        user_id=user_a.id,
        quotation=quote_a,
        party=party_a,
    )
    session.add(ship_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")
    party_b = _party(organization_id=org_b.id, legal_name="Klient B", created_by=user_b.id)
    session.add_all([rate_b, party_b])
    await session.flush()
    quote_b = _quote(
        organization_id=org_b.id,
        created_by=user_b.id,
        rate_line_id=rate_b.id,
        source_ref="tariff://b",
    )
    session.add(quote_b)
    await session.flush()
    ship_b = _shipment(
        organization_id=org_b.id,
        user_id=user_b.id,
        quotation=quote_b,
        party=party_b,
    )
    session.add(ship_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Shipment))).all())
    assert {row.id for row in visible_a} == {ship_a.id}
    foreign_b = await session.scalar(select(Shipment).where(Shipment.id == ship_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Shipment))).all())
    assert {row.id for row in visible_b} == {ship_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_rejects_foreign_quotation(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

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

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    stolen = Shipment(
        id=uuid4(),
        organization_id=org_a.id,
        quotation_id=quote_b.id,
        party_id=party_a.id,
        source_ref="fixture://shipment/stolen",
        status="draft",
        created_by=user_a.id,
    )
    session.add(stolen)
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_rejects_second_row_for_same_quotation(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]

    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add_all([rate_a, party_a])
    await session.flush()
    quote_a = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a",
    )
    session.add(quote_a)
    await session.flush()
    session.add(
        _shipment(
            organization_id=org_a.id,
            user_id=user_a.id,
            quotation=quote_a,
            party=party_a,
        )
    )
    await session.flush()
    session.add(
        Shipment(
            id=uuid4(),
            organization_id=org_a.id,
            quotation_id=quote_a.id,
            party_id=party_a.id,
            source_ref="fixture://shipment/dup",
            status="draft",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_ref_unique_per_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add_all([rate_a, party_a])
    await session.flush()
    quote_one = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a1",
    )
    quote_two = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a2",
    )
    session.add_all([quote_one, quote_two])
    await session.flush()
    session.add(
        _shipment(
            organization_id=org_a.id,
            user_id=user_a.id,
            quotation=quote_one,
            party=party_a,
            shipment_ref="omni://shipment/ab1",
        )
    )
    await session.flush()
    session.add(
        _shipment(
            organization_id=org_a.id,
            user_id=user_a.id,
            quotation=quote_two,
            party=party_a,
            shipment_ref="omni://shipment/ab1",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_ref_same_token_two_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    token = "fixture://shipment-ref/shared"
    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add_all([rate_a, party_a])
    await session.flush()
    quote_a = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a",
    )
    session.add(quote_a)
    await session.flush()
    session.add(
        _shipment(
            organization_id=org_a.id,
            user_id=user_a.id,
            quotation=quote_a,
            party=party_a,
            shipment_ref=token,
        )
    )
    await session.flush()

    await bind_tenant(session, org_b.id)
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")
    party_b = _party(organization_id=org_b.id, legal_name="Klient B", created_by=user_b.id)
    session.add_all([rate_b, party_b])
    await session.flush()
    quote_b = _quote(
        organization_id=org_b.id,
        created_by=user_b.id,
        rate_line_id=rate_b.id,
        source_ref="tariff://b",
    )
    session.add(quote_b)
    await session.flush()
    session.add(
        _shipment(
            organization_id=org_b.id,
            user_id=user_b.id,
            quotation=quote_b,
            party=party_b,
            shipment_ref=token,
        )
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(Shipment))).all())
    assert len(visible) == 1
    assert visible[0].shipment_ref == token
