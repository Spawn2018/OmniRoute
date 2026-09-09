from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.core.database import bind_tenant
from app.models.rate_card import RateCard


def _card(*, organization_id, created_by, code: str, when: str, amount: str):
    return RateCard(
        id=uuid4(),
        organization_id=organization_id,
        card_code=code,
        applies_when=when,
        amount=Decimal(amount),
        currency="EUR",
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_card_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _card(
        organization_id=org_a.id,
        created_by=user_a.id,
        code="weekend",
        when="sobota",
        amount="10.0000",
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _card(
        organization_id=org_b.id,
        created_by=user_b.id,
        code="weekday",
        when="poniedzialek",
        amount="12.0000",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(RateCard))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(RateCard).where(RateCard.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(RateCard))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_card_equal_when_hides_other_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    await bind_tenant(session, org_a.id)
    session.add(
        _card(
            organization_id=org_a.id,
            created_by=user_a.id,
            code="weekend",
            when="sobota",
            amount="10.0000",
        )
    )
    await session.flush()
    await bind_tenant(session, org_b.id)
    session.add(
        _card(
            organization_id=org_b.id,
            created_by=user_b.id,
            code="weekend",
            when="sobota",
            amount="11.0000",
        )
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list(
        (
            await session.scalars(select(RateCard).where(RateCard.applies_when == "sobota"))
        ).all()
    )
    assert len(visible) == 1
    assert visible[0].organization_id == org_a.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_card_equal_when_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'rate_card' "
            "AND indexname = 'ix_rate_card_org_when'"
        ),
    )
    assert named.first() is not None
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM rate_card "
            "WHERE organization_id = :org_id AND applies_when = :when_token"
        ),
        {"org_id": org_a.id, "when_token": "sobota"},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_rate_card_org_when" in joined or "Index Scan" in joined
