from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.commodity_code import CommodityCode
from app.models.customer_rfq import CustomerRfq
from app.models.dangerous_good import DangerousGood
from app.models.inbound_message import InboundMessage
from app.models.party import Party
from app.models.port import Port
from app.models.quotation import Quotation
from app.models.rate_line import RateLine

_UNLOCODE_SOURCE = "github:cristan/improved-un-locodes@fixture"


def _message(*, organization_id, user_id, suffix: str) -> InboundMessage:
    return InboundMessage(
        id=uuid4(),
        organization_id=organization_id,
        source_ref=f"fixture://inbound-mail/{suffix}",
        from_address=f"ops-{suffix}@carrier.example",
        subject=f"RFQ {suffix}",
        body_text=f"treść {suffix}",
        status="draft",
        created_by=user_id,
    )


def _party(*, organization_id, created_by, legal_name: str) -> Party:
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_may_not_point_rfq_at_another_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    mail_b = _message(organization_id=org_b.id, user_id=user_b.id, suffix="b")
    session.add(mail_b)
    await session.flush()
    rfq_b = CustomerRfq(
        id=uuid4(),
        organization_id=org_b.id,
        inbound_message_id=mail_b.id,
        source_ref=mail_b.source_ref,
        status="draft",
        created_by=user_b.id,
    )
    session.add(rfq_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    origin = _port(organization_id=org_a.id, unlocode="PLGDY")
    destination = _port(organization_id=org_a.id, unlocode="DEHAM")
    party = _party(organization_id=org_a.id, created_by=user_a.id, legal_name="ACME A")
    rate = RateLine(
        id=uuid4(),
        organization_id=org_a.id,
        charge_code="THC",
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
        created_by=user_a.id,
    )
    session.add_all([origin, destination, party, rate])
    await session.flush()
    session.add(
        Quotation(
            id=uuid4(),
            organization_id=org_a.id,
            charge_code="THC",
            rate_line_id=rate.id,
            amount=Decimal("10.0000"),
            currency="EUR",
            source_ref="tariff://a",
            created_by=user_a.id,
            origin_port_id=origin.id,
            destination_port_id=destination.id,
            party_id=party.id,
            customer_rfq_id=rfq_b.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_quotation_customer_rfq"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_may_not_point_hs_at_another_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    code_b = CommodityCode(
        id=uuid4(),
        organization_id=org_b.id,
        code="0901",
        name="Coffee B",
        aliases=[],
        source_ref="tenant:manual",
        created_by=user_b.id,
    )
    session.add(code_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    origin = _port(organization_id=org_a.id, unlocode="PLGDY")
    destination = _port(organization_id=org_a.id, unlocode="DEHAM")
    party = _party(organization_id=org_a.id, created_by=user_a.id, legal_name="ACME A")
    rate = RateLine(
        id=uuid4(),
        organization_id=org_a.id,
        charge_code="THC",
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
        created_by=user_a.id,
    )
    session.add_all([origin, destination, party, rate])
    await session.flush()
    session.add(
        Quotation(
            id=uuid4(),
            organization_id=org_a.id,
            charge_code="THC",
            rate_line_id=rate.id,
            amount=Decimal("10.0000"),
            currency="EUR",
            source_ref="tariff://a",
            created_by=user_a.id,
            origin_port_id=origin.id,
            destination_port_id=destination.id,
            party_id=party.id,
            commodity_code_id=code_b.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_quotation_commodity_code"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_may_not_point_un_at_another_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    good_b = DangerousGood(
        id=uuid4(),
        organization_id=org_b.id,
        un_number="1263",
        imdg_class="3",
        adr_tunnel_code="D",
        segregation_group="none",
        packing_group="II",
        marine_pollutant=False,
        name="Paint B",
        aliases=[],
        source_ref="tenant:manual",
        created_by=user_b.id,
    )
    session.add(good_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    origin = _port(organization_id=org_a.id, unlocode="PLGDN")
    destination = _port(organization_id=org_a.id, unlocode="NLRTM")
    party = _party(organization_id=org_a.id, created_by=user_a.id, legal_name="ACME UN")
    rate = RateLine(
        id=uuid4(),
        organization_id=org_a.id,
        charge_code="BAF",
        amount=Decimal("11.0000"),
        currency="USD",
        source_ref="tariff://un",
        created_by=user_a.id,
    )
    session.add_all([origin, destination, party, rate])
    await session.flush()
    session.add(
        Quotation(
            id=uuid4(),
            organization_id=org_a.id,
            charge_code="BAF",
            rate_line_id=rate.id,
            amount=Decimal("11.0000"),
            currency="USD",
            source_ref="tariff://un",
            created_by=user_a.id,
            origin_port_id=origin.id,
            destination_port_id=destination.id,
            party_id=party.id,
            dangerous_good_id=good_b.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_quotation_dangerous_good"):
        await session.flush()
