from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.incoterm_responsibility import IncotermResponsibility


@pytest.mark.integration
@pytest.mark.asyncio
async def test_incoterm_responsibility_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = IncotermResponsibility(
        id=uuid4(),
        organization_id=org_a.id,
        incoterm="FOB",
        trade_side="export",
        export_clearance_role="seller",
        import_clearance_role="buyer",
        main_carriage_booker="buyer",
        booking_scope=["ocean"],
        source_ref="fixture://incoterm-responsibility/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = IncotermResponsibility(
        id=uuid4(),
        organization_id=org_b.id,
        incoterm="DDP",
        trade_side="import",
        export_clearance_role="seller",
        import_clearance_role="seller",
        main_carriage_booker="seller",
        booking_scope=["ocean", "oncarriage"],
        source_ref="fixture://incoterm-responsibility/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(IncotermResponsibility))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(IncotermResponsibility).where(IncotermResponsibility.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(IncotermResponsibility))).all())
    assert {row.id for row in visible_b} == {row_b.id}
