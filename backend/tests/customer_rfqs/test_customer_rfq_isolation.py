from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.commodity_code import CommodityCode
from app.models.customer_rfq import CustomerRfq
from app.models.dangerous_good import DangerousGood
from app.models.inbound_message import InboundMessage


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


def _rfq(*, organization_id, user_id, message: InboundMessage) -> CustomerRfq:
    return CustomerRfq(
        id=uuid4(),
        organization_id=organization_id,
        inbound_message_id=message.id,
        source_ref=message.source_ref,
        status="draft",
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_rfq_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    mail_a = _message(organization_id=org_a.id, user_id=user_a.id, suffix="a")
    mail_b = _message(organization_id=org_b.id, user_id=user_b.id, suffix="b")
    rfq_a = _rfq(organization_id=org_a.id, user_id=user_a.id, message=mail_a)
    rfq_b = _rfq(organization_id=org_b.id, user_id=user_b.id, message=mail_b)

    await bind_tenant(session, org_a.id)
    session.add(mail_a)
    await session.flush()
    session.add(rfq_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(mail_b)
    await session.flush()
    session.add(rfq_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CustomerRfq))).all())
    assert {row.id for row in visible_a} == {rfq_a.id}
    foreign_b = await session.scalar(select(CustomerRfq).where(CustomerRfq.id == rfq_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CustomerRfq))).all())
    assert {row.id for row in visible_b} == {rfq_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_rfq_rejects_foreign_inbound_message(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    mail_b = _message(organization_id=org_b.id, user_id=user_b.id, suffix="b")
    await bind_tenant(session, org_b.id)
    session.add(mail_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    stolen = CustomerRfq(
        id=uuid4(),
        organization_id=org_a.id,
        inbound_message_id=mail_b.id,
        source_ref=mail_b.source_ref,
        status="draft",
        created_by=user_a.id,
    )
    session.add(stolen)
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_rfq_rejects_foreign_commodity_code(session, two_tenants) -> None:
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
    mail_a = _message(organization_id=org_a.id, user_id=user_a.id, suffix="a-hs")
    session.add(mail_a)
    await session.flush()
    session.add(
        CustomerRfq(
            id=uuid4(),
            organization_id=org_a.id,
            inbound_message_id=mail_a.id,
            source_ref=mail_a.source_ref,
            status="draft",
            created_by=user_a.id,
            commodity_code_id=code_b.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_customer_rfq_commodity_code"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_rfq_rejects_foreign_dangerous_good(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    good_b = DangerousGood(
        id=uuid4(),
        organization_id=org_b.id,
        un_number="1203",
        imdg_class="3",
        adr_tunnel_code="D",
        segregation_group="none",
        packing_group="II",
        name="Petrol B",
        aliases=[],
        source_ref="tenant:manual",
        created_by=user_b.id,
    )
    session.add(good_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    mail_a = _message(organization_id=org_a.id, user_id=user_a.id, suffix="a-un")
    session.add(mail_a)
    await session.flush()
    session.add(
        CustomerRfq(
            id=uuid4(),
            organization_id=org_a.id,
            inbound_message_id=mail_a.id,
            source_ref=mail_a.source_ref,
            status="draft",
            created_by=user_a.id,
            dangerous_good_id=good_b.id,
        )
    )
    with pytest.raises(IntegrityError, match="fk_customer_rfq_dangerous_good"):
        await session.flush()
