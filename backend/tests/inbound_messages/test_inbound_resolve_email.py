from uuid import uuid4

import pytest

from app.core.database import bind_tenant
from app.domain.errors import UnknownEmailDomain
from app.models.inbound_message import InboundMessage
from app.models.party import Party
from app.models.party_email_domain import PartyEmailDomain
from app.services.inbound_messages.inbound_message_service import InboundMessageService
from app.services.parties.party_service import PartyService


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
async def test_resolve_email_attaches_same_tenant_party(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    party = Party(
        id=uuid4(),
        organization_id=org_a.id,
        legal_name="Carrier A",
        country_code="PL",
        roles=["customer"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=user_a.id,
    )
    domain = PartyEmailDomain(
        id=uuid4(),
        organization_id=org_a.id,
        party_id=party.id,
        domain="carrier.example",
        source_ref="tenant:manual",
        created_by=user_a.id,
    )
    mail = _message(organization_id=org_a.id, user_id=user_a.id, suffix="a")
    mail.from_address = "ops-a@carrier.example"

    await bind_tenant(session, org_a.id)
    session.add(party)
    await session.flush()
    session.add(domain)
    session.add(mail)
    await session.flush()

    party_row = await PartyService(session).resolve_email(mail.from_address)
    attached = await InboundMessageService(session).attach_party(mail.id, party_row.id)
    assert attached.party_id == party.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_email_unknown_domain_does_not_create_party(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    mail = _message(organization_id=org_a.id, user_id=user_a.id, suffix="a")
    await bind_tenant(session, org_a.id)
    session.add(mail)
    await session.flush()
    with pytest.raises(UnknownEmailDomain):
        await PartyService(session).resolve_email(mail.from_address)
