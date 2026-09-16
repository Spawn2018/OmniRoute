from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.margin_floor import MarginFloor


def _row(
    *,
    organization_id,
    created_by,
    floor_code: str = "floor_gdn_ham",
    source_ref: str = "tenant:manual",
) -> MarginFloor:
    return MarginFloor(
        id=uuid4(),
        organization_id=organization_id,
        floor_code=floor_code,
        origin_unlocode="PLGDN",
        destination_unlocode="DEHAM",
        floor_amount=Decimal("120.0000"),
        floor_currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_margin_floor_rls_isolates_tenants(
    session,
    two_tenants,
) -> None:
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
        floor_code="floor_waw_ber",
        source_ref="fixture://margin-floor/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(MarginFloor))).all())
    assert {row.id for row in visible_a} == {row_a.id}

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(MarginFloor))).all())
    assert {row.id for row in visible_b} == {row_b.id}
