from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.quotation import Quotation
from app.models.rate_line import RateLine
from app.models.tender_quote import TenderQuote


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


def _bid(*, organization_id, created_by, quotation_id, limit: int) -> TenderQuote:
    return TenderQuote(
        id=uuid4(),
        organization_id=organization_id,
        quotation_id=quotation_id,
        valid_until=date(2026, 12, 31),
        order_limit=limit,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_quote_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(
        organization_id=org_a.id,
        created_by=user_a.id,
        source_ref="fixture://rate-line/ta",
    )
    session.add(rate_a)
    await session.flush()
    quote_a = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="fixture://quotation/ta",
    )
    session.add(quote_a)
    await session.flush()
    row_a = _bid(
        organization_id=org_a.id,
        created_by=user_a.id,
        quotation_id=quote_a.id,
        limit=2,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    rate_b = _buy_rate(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://rate-line/tb",
    )
    session.add(rate_b)
    await session.flush()
    quote_b = _quote(
        organization_id=org_b.id,
        created_by=user_b.id,
        rate_line_id=rate_b.id,
        source_ref="fixture://quotation/tb",
    )
    session.add(quote_b)
    await session.flush()
    row_b = _bid(
        organization_id=org_b.id,
        created_by=user_b.id,
        quotation_id=quote_b.id,
        limit=4,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(TenderQuote))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(TenderQuote).where(TenderQuote.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(TenderQuote))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_quote_rejects_foreign_quotation(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    rate_b = _buy_rate(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://rate-line/tx",
    )
    session.add(rate_b)
    await session.flush()
    quote_b = _quote(
        organization_id=org_b.id,
        created_by=user_b.id,
        rate_line_id=rate_b.id,
        source_ref="fixture://quotation/tx",
    )
    session.add(quote_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        _bid(
            organization_id=org_a.id,
            created_by=user_a.id,
            quotation_id=quote_b.id,
            limit=1,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_quote_list_uses_org_quotation_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM tender_quote "
            "WHERE organization_id = :org_id AND quotation_id = :quote_id"
        ),
        {"org_id": org_a.id, "quote_id": uuid4()},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_tender_quote_org_quotation" in joined
