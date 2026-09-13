from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.benefit_ledger import BenefitLedger


def _row(
    *,
    organization_id,
    created_by,
    source_ref: str = "fixture://benefit-ledger/",
    benefit_code: str = "dock_save",
) -> BenefitLedger:
    return BenefitLedger(
        id=uuid4(),
        organization_id=organization_id,
        benefit_code=benefit_code,
        method_label="porownanie z wczorajszym charge",
        hours_saved=Decimal("2.5000"),
        saved_amount=Decimal("150.0000"),
        saved_currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_benefit_ledger_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        benefit_code="fuel_cut",
        source_ref="fixture://benefit-ledger/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(BenefitLedger))).all())
    assert {row.id for row in visible} == {row_a.id}
