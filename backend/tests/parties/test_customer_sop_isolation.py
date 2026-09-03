from uuid import uuid4

import pytest
from sqlalchemy import select

from datetime import UTC, datetime

from app.core.database import bind_tenant
from app.domain.errors import UnknownParty
from app.models.customer_sop import CustomerSop
from app.models.party import Party
from app.services.parties.party_service import PartyService

_MANUAL = "tenant:manual"


def _party(*, organization_id, legal_name: str, created_by):
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


def _sop(*, organization_id, party_id, code: str, created_by):
    return CustomerSop(
        id=uuid4(),
        organization_id=organization_id,
        party_id=party_id,
        status="draft",
        code=code,
        title=code.replace("_", " "),
        body="treść procedury operacyjnej klienta",
        source_ref=_MANUAL,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_sop_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    sop_a = _sop(
        organization_id=org_a.id,
        party_id=party_a.id,
        code="pre_alert",
        created_by=user_a.id,
    )
    session.add(sop_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Klient B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    sop_b = _sop(
        organization_id=org_b.id,
        party_id=party_b.id,
        code="pre_alert",
        created_by=user_b.id,
    )
    session.add(sop_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CustomerSop))).all())
    assert {row.id for row in visible_a} == {sop_a.id}
    assert await session.scalar(select(CustomerSop).where(CustomerSop.id == sop_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CustomerSop))).all())
    assert {row.id for row in visible_b} == {sop_b.id}
    assert await session.scalar(select(CustomerSop).where(CustomerSop.id == sop_a.id)) is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_auto_block_does_not_see_other_tenant_sop(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    sop_a = _sop(
        organization_id=org_a.id,
        party_id=party_a.id,
        code="no_auto",
        created_by=user_a.id,
    )
    sop_a.status = "approved"
    sop_a.approved_at = datetime.now(UTC)
    sop_a.blocks_auto = True
    session.add(sop_a)
    await session.flush()
    assert await PartyService(session).party_blocks_auto(party_a.id) is True
    session.expunge_all()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Klient B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    with pytest.raises(UnknownParty):
        await PartyService(session).party_blocks_auto(party_a.id)
    assert await PartyService(session).party_blocks_auto(party_b.id) is False
