from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.tender import Tender
from app.models.tender_consortium_member import TenderConsortiumMember


def _party(*, organization_id, legal_name: str, created_by) -> Party:
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["agent"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=created_by,
    )


def _board(*, organization_id, created_by, buyer_party_id) -> Tender:
    return Tender(
        id=uuid4(),
        organization_id=organization_id,
        side="sell",
        kind="open",
        status="draft",
        buyer_party_id=buyer_party_id,
        deadline_at=date(2026, 12, 31),
        incoterm="FOB",
        trade_side="export",
        named_place="Gdynia",
        source_ref="tenant:manual",
        created_by=created_by,
    )


def _seat(
    *,
    organization_id,
    created_by,
    tender_id,
    party_id,
    seat_code: str = "lead",
) -> TenderConsortiumMember:
    return TenderConsortiumMember(
        id=uuid4(),
        organization_id=organization_id,
        tender_id=tender_id,
        party_id=party_id,
        seat_code=seat_code,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_consortium_member_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    buyer_a = _party(organization_id=org_a.id, legal_name="Buyer A", created_by=user_a.id)
    member_a = _party(organization_id=org_a.id, legal_name="Seat A", created_by=user_a.id)
    session.add_all([buyer_a, member_a])
    await session.flush()
    board_a = _board(
        organization_id=org_a.id,
        created_by=user_a.id,
        buyer_party_id=buyer_a.id,
    )
    session.add(board_a)
    await session.flush()
    row_a = _seat(
        organization_id=org_a.id,
        created_by=user_a.id,
        tender_id=board_a.id,
        party_id=member_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    buyer_b = _party(organization_id=org_b.id, legal_name="Buyer B", created_by=user_b.id)
    member_b = _party(organization_id=org_b.id, legal_name="Seat B", created_by=user_b.id)
    session.add_all([buyer_b, member_b])
    await session.flush()
    board_b = _board(
        organization_id=org_b.id,
        created_by=user_b.id,
        buyer_party_id=buyer_b.id,
    )
    session.add(board_b)
    await session.flush()
    row_b = _seat(
        organization_id=org_b.id,
        created_by=user_b.id,
        tender_id=board_b.id,
        party_id=member_b.id,
        seat_code="member",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(TenderConsortiumMember))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert (
        await session.scalar(
            select(TenderConsortiumMember).where(TenderConsortiumMember.id == row_b.id),
        )
        is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(TenderConsortiumMember))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_consortium_member_rejects_foreign_tender(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    buyer_b = _party(organization_id=org_b.id, legal_name="Buyer X", created_by=user_b.id)
    session.add(buyer_b)
    await session.flush()
    board_b = _board(
        organization_id=org_b.id,
        created_by=user_b.id,
        buyer_party_id=buyer_b.id,
    )
    session.add(board_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    member_a = _party(organization_id=org_a.id, legal_name="Seat A", created_by=user_a.id)
    session.add(member_a)
    await session.flush()
    session.add(
        _seat(
            organization_id=org_a.id,
            created_by=user_a.id,
            tender_id=board_b.id,
            party_id=member_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_consortium_member_rejects_foreign_party(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Seat X", created_by=user_b.id)
    session.add(party_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    buyer_a = _party(organization_id=org_a.id, legal_name="Buyer A", created_by=user_a.id)
    session.add(buyer_a)
    await session.flush()
    board_a = _board(
        organization_id=org_a.id,
        created_by=user_a.id,
        buyer_party_id=buyer_a.id,
    )
    session.add(board_a)
    await session.flush()
    session.add(
        _seat(
            organization_id=org_a.id,
            created_by=user_a.id,
            tender_id=board_a.id,
            party_id=party_b.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_consortium_member_list_uses_org_tender_index(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM tender_consortium_member "
            "WHERE organization_id = :org_id AND tender_id = :tender_id"
        ),
        {"org_id": org_a.id, "tender_id": uuid4()},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_tender_consortium_member_org_tender" in joined
        or "uq_tender_consortium_member_org_tender_party" in joined
    )
