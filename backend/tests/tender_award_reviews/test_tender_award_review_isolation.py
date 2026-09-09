from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.tender import Tender
from app.models.tender_award_review import TenderAwardReview


def _party(*, organization_id, legal_name: str, created_by) -> Party:
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


def _review(
    *,
    organization_id,
    created_by,
    tender_id,
    review_code: str = "countersign",
) -> TenderAwardReview:
    return TenderAwardReview(
        id=uuid4(),
        organization_id=organization_id,
        tender_id=tender_id,
        review_code=review_code,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_award_review_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Buyer A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    board_a = _board(
        organization_id=org_a.id,
        created_by=user_a.id,
        buyer_party_id=party_a.id,
    )
    session.add(board_a)
    await session.flush()
    row_a = _review(
        organization_id=org_a.id,
        created_by=user_a.id,
        tender_id=board_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Buyer B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    board_b = _board(
        organization_id=org_b.id,
        created_by=user_b.id,
        buyer_party_id=party_b.id,
    )
    session.add(board_b)
    await session.flush()
    row_b = _review(
        organization_id=org_b.id,
        created_by=user_b.id,
        tender_id=board_b.id,
        review_code="challenge",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(TenderAwardReview))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert (
        await session.scalar(
            select(TenderAwardReview).where(TenderAwardReview.id == row_b.id),
        )
        is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(TenderAwardReview))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_award_review_rejects_foreign_tender(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Buyer X", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    board_b = _board(
        organization_id=org_b.id,
        created_by=user_b.id,
        buyer_party_id=party_b.id,
    )
    session.add(board_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        _review(
            organization_id=org_a.id,
            created_by=user_a.id,
            tender_id=board_b.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_award_review_list_uses_org_code_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM tender_award_review "
            "WHERE organization_id = :org_id AND review_code = :code"
        ),
        {"org_id": org_a.id, "code": "countersign"},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_tender_award_review_org_code" in joined
        or "uq_tender_award_review_org_tender" in joined
    )
