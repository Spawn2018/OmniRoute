from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.purchase_order import PurchaseOrder


def _header(
    *,
    organization_id,
    created_by,
    po_code: str = "po_gdansk_01",
    plant_label: str | None = "Gdańsk",
    source_ref: str = "tenant:manual",
) -> PurchaseOrder:
    return PurchaseOrder(
        id=uuid4(),
        organization_id=organization_id,
        po_code=po_code,
        plant_label=plant_label,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_purchase_order_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    header_a = _header(organization_id=org_a.id, created_by=user_a.id)
    session.add(header_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    header_b = _header(
        organization_id=org_b.id,
        created_by=user_b.id,
        po_code="po_berlin_01",
        plant_label=None,
        source_ref="fixture://purchase-order/b",
    )
    session.add(header_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PurchaseOrder))).all())
    assert {row.id for row in visible_a} == {header_a.id}
    hidden = await session.scalar(select(PurchaseOrder).where(PurchaseOrder.id == header_b.id))
    assert hidden is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PurchaseOrder))).all())
    assert {row.id for row in visible_b} == {header_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_purchase_order_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_header(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _header(
            organization_id=org_a.id,
            created_by=user_a.id,
            po_code="po_gdansk_02",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_purchase_order_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_header(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _header(
            organization_id=org_a.id,
            created_by=user_a.id,
            source_ref="fixture://purchase-order/dup-code",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_purchase_order_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM purchase_order WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_purchase_order_organization_id" in joined
        or "uq_purchase_order_org_id" in joined
        or "uq_purchase_order_org_source_ref" in joined
        or "uq_purchase_order_org_code" in joined
        or "Index Scan" in joined
    )
