from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.credit_review import CreditReview
from app.models.party import Party

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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_credit_review_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Klient A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    review_a = CreditReview(
        id=uuid4(),
        organization_id=org_a.id,
        decision="ok",
        review_date=date(2026, 9, 1),
        party_id=party_a.id,
        note=None,
        source_ref=_MANUAL,
        created_by=user_a.id,
    )
    session.add(review_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Klient B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    review_b = CreditReview(
        id=uuid4(),
        organization_id=org_b.id,
        decision="hold",
        review_date=date(2026, 9, 1),
        party_id=party_b.id,
        note=None,
        source_ref=_MANUAL,
        created_by=user_b.id,
    )
    session.add(review_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CreditReview))).all())
    assert {row.id for row in visible_a} == {review_a.id}
    assert await session.scalar(select(CreditReview).where(CreditReview.id == review_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CreditReview))).all())
    assert {row.id for row in visible_b} == {review_b.id}
    assert await session.scalar(select(CreditReview).where(CreditReview.id == review_a.id)) is None
