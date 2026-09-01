from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.nbp_rate import NbpRate
from app.services.nbp_rates.nbp_rate_service import NbpRateService


def _rate(
    *,
    organization_id: UUID,
    user_id: UUID,
    currency: str,
    rate_date: date,
    mid: str,
) -> NbpRate:
    return NbpRate(
        id=uuid4(),
        organization_id=organization_id,
        currency=currency,
        rate_date=rate_date,
        mid=Decimal(mid),
        source_ref=f"nbp:A:{rate_date.isoformat()}:042",
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_nbp_rate_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    day = date(2026, 9, 1)

    rate_a = _rate(
        organization_id=org_a.id,
        user_id=user_a.id,
        currency="EUR",
        rate_date=day,
        mid="4.2500",
    )
    rate_b = _rate(
        organization_id=org_b.id,
        user_id=user_b.id,
        currency="EUR",
        rate_date=day,
        mid="4.2600",
    )

    await bind_tenant(session, org_a.id)
    session.add(rate_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(rate_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(NbpRate))).all())
    assert {row.id for row in visible_a} == {rate_a.id}
    foreign_b = await session.scalar(select(NbpRate).where(NbpRate.id == rate_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(NbpRate))).all())
    assert {row.id for row in visible_b} == {rate_b.id}
    foreign_a = await session.scalar(select(NbpRate).where(NbpRate.id == rate_a.id))
    assert foreign_a is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_picks_latest_rate_on_or_before_date(session, two_tenants) -> None:
    org = two_tenants["org_a"]
    user = two_tenants["user_a"]
    await bind_tenant(session, org.id)
    session.add(
        _rate(
            organization_id=org.id,
            user_id=user.id,
            currency="USD",
            rate_date=date(2026, 8, 28),
            mid="3.9000",
        ),
    )
    later = _rate(
        organization_id=org.id,
        user_id=user.id,
        currency="USD",
        rate_date=date(2026, 9, 1),
        mid="3.9500",
    )
    session.add(later)
    await session.flush()

    service = NbpRateService(session)
    weekend = await service.resolve("USD", date(2026, 9, 5))
    assert weekend.id == later.id
    assert weekend.mid == Decimal("3.9500")
    friday = await service.resolve("usd", date(2026, 8, 28))
    assert friday.rate_date == date(2026, 8, 28)
    assert friday.mid == Decimal("3.9000")
