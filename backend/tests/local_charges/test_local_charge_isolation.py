from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.core.database import bind_tenant
from app.models.local_charge import LocalCharge


def _row(*, organization_id, created_by, kind: str, amount: str) -> LocalCharge:
    return LocalCharge(
        id=uuid4(),
        organization_id=organization_id,
        charge_kind=kind,
        amount=Decimal(amount),
        currency="EUR",
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_local_charge_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(organization_id=org_a.id, created_by=user_a.id, kind="thc", amount="80.0000")
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(organization_id=org_b.id, created_by=user_b.id, kind="isps", amount="25.0000")
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(LocalCharge))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(LocalCharge).where(LocalCharge.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(LocalCharge))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_local_charge_list_uses_org_kind_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM local_charge "
            "WHERE organization_id = :org_id AND charge_kind = :kind"
        ),
        {"org_id": org_a.id, "kind": "thc"},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_local_charge_org_kind" in joined
