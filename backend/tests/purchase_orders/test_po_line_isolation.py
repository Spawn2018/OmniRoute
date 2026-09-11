from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.domain.errors import ResourceNotFound
from app.models.po_line import PoLine
from app.models.purchase_order import PurchaseOrder
from app.services.purchase_orders.po_line_service import PoLineService


def _header(
    *,
    organization_id,
    created_by,
    po_code: str = "po_gdansk_01",
    source_ref: str = "tenant:manual",
) -> PurchaseOrder:
    return PurchaseOrder(
        id=uuid4(),
        organization_id=organization_id,
        po_code=po_code,
        plant_label=None,
        source_ref=source_ref,
        created_by=created_by,
    )


def _line(
    *,
    organization_id,
    created_by,
    purchase_order_id,
    line_code: str = "line_01",
    source_ref: str = "tenant:manual",
) -> PoLine:
    return PoLine(
        id=uuid4(),
        organization_id=organization_id,
        purchase_order_id=purchase_order_id,
        line_code=line_code,
        sku_code="SKU-4401",
        qty=Decimal("12.5000"),
        uom_code="pcs",
        plant_label=None,
        batch_label=None,
        serial_label=None,
        coo_label=None,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_po_line_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    header_a = _header(organization_id=org_a.id, created_by=user_a.id)
    session.add(header_a)
    await session.flush()
    line_a = _line(
        organization_id=org_a.id,
        created_by=user_a.id,
        purchase_order_id=header_a.id,
    )
    session.add(line_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    header_b = _header(
        organization_id=org_b.id,
        created_by=user_b.id,
        po_code="po_berlin_01",
        source_ref="fixture://purchase-order/b",
    )
    session.add(header_b)
    await session.flush()
    line_b = _line(
        organization_id=org_b.id,
        created_by=user_b.id,
        purchase_order_id=header_b.id,
        line_code="line_99",
        source_ref="fixture://po-line/b",
    )
    session.add(line_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PoLine))).all())
    assert {row.id for row in visible_a} == {line_a.id}
    hidden = await session.scalar(select(PoLine).where(PoLine.id == line_b.id))
    assert hidden is None
    foreign_header = await session.scalar(
        select(PurchaseOrder).where(PurchaseOrder.id == header_b.id)
    )
    assert foreign_header is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PoLine))).all())
    assert {row.id for row in visible_b} == {line_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_po_line_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    header = _header(organization_id=org_a.id, created_by=user_a.id)
    session.add(header)
    await session.flush()
    session.add(
        _line(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
        )
    )
    await session.flush()
    session.add(
        _line(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
            line_code="line_02",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_po_line_rejects_duplicate_line_on_header(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    header = _header(organization_id=org_a.id, created_by=user_a.id)
    session.add(header)
    await session.flush()
    session.add(
        _line(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
        )
    )
    await session.flush()
    session.add(
        _line(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
            source_ref="fixture://po-line/dup-line",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_po_line_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM po_line WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_po_line_organization_id" in joined
        or "uq_po_line_org_id" in joined
        or "uq_po_line_org_source_ref" in joined
        or "uq_po_line_org_header_line" in joined
        or "Index Scan" in joined
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_po_line_rejects_foreign_header(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    header_b = _header(
        organization_id=org_b.id,
        created_by=user_b.id,
        po_code="po_berlin_01",
        source_ref="fixture://purchase-order/b",
    )
    session.add(header_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    with pytest.raises(ResourceNotFound, match="nieznane zamówienie"):
        await PoLineService(session).persist_po_line(
            organization_id=org_a.id,
            user_id=user_a.id,
            purchase_order_id=header_b.id,
            line_code="line_01",
            sku_code="SKU-4401",
            qty="1",
            uom_code="pcs",
            plant_label=None,
            batch_label=None,
            serial_label=None,
            coo_label=None,
            source_ref="fixture://po-line/cross",
        )
