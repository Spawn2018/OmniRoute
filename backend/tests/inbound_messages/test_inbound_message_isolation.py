from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.inbound_message import InboundMessage
from app.models.party import Party


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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_inbound_message_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    mail_a = _message(organization_id=org_a.id, user_id=user_a.id, suffix="a")
    mail_b = _message(organization_id=org_b.id, user_id=user_b.id, suffix="b")

    await bind_tenant(session, org_a.id)
    session.add(mail_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(mail_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(InboundMessage))).all())
    assert {row.id for row in visible_a} == {mail_a.id}
    foreign_b = await session.scalar(
        select(InboundMessage).where(InboundMessage.id == mail_b.id),
    )
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(InboundMessage))).all())
    assert {row.id for row in visible_b} == {mail_b.id}
    foreign_a = await session.scalar(
        select(InboundMessage).where(InboundMessage.id == mail_a.id),
    )
    assert foreign_a is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_inbound_message_rejects_foreign_party_id(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    party_b = Party(
        id=uuid4(),
        organization_id=org_b.id,
        legal_name="B",
        country_code="PL",
        roles=["customer"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=user_b.id,
    )
    mail_a = _message(organization_id=org_a.id, user_id=user_a.id, suffix="a")

    await bind_tenant(session, org_b.id)
    session.add(party_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(mail_a)
    await session.flush()
    mail_a.party_id = party_b.id
    with pytest.raises(IntegrityError):
        await session.flush()
