from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.domain.errors import ResourceNotFound
from app.models.asn import Asn
from app.models.purchase_order import PurchaseOrder
from app.services.purchase_orders.asn_service import AsnService


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


def _notice(
    *,
    organization_id,
    created_by,
    purchase_order_id,
    asn_code: str = "asn_01",
    source_ref: str = "tenant:manual",
) -> Asn:
    return Asn(
        id=uuid4(),
        organization_id=organization_id,
        purchase_order_id=purchase_order_id,
        asn_code=asn_code,
        plant_label=None,
        carrier_label=None,
        ship_ref_label=None,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_asn_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    header_a = _header(organization_id=org_a.id, created_by=user_a.id)
    session.add(header_a)
    await session.flush()
    notice_a = _notice(
        organization_id=org_a.id,
        created_by=user_a.id,
        purchase_order_id=header_a.id,
    )
    session.add(notice_a)
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
    notice_b = _notice(
        organization_id=org_b.id,
        created_by=user_b.id,
        purchase_order_id=header_b.id,
        asn_code="asn_99",
        source_ref="fixture://asn/b",
    )
    session.add(notice_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Asn))).all())
    assert {row.id for row in visible_a} == {notice_a.id}
    hidden = await session.scalar(select(Asn).where(Asn.id == notice_b.id))
    assert hidden is None
    foreign_header = await session.scalar(
        select(PurchaseOrder).where(PurchaseOrder.id == header_b.id)
    )
    assert foreign_header is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Asn))).all())
    assert {row.id for row in visible_b} == {notice_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_asn_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    header = _header(organization_id=org_a.id, created_by=user_a.id)
    session.add(header)
    await session.flush()
    session.add(
        _notice(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
        )
    )
    await session.flush()
    session.add(
        _notice(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
            asn_code="asn_02",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_asn_rejects_duplicate_code_on_header(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    header = _header(organization_id=org_a.id, created_by=user_a.id)
    session.add(header)
    await session.flush()
    session.add(
        _notice(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
        )
    )
    await session.flush()
    session.add(
        _notice(
            organization_id=org_a.id,
            created_by=user_a.id,
            purchase_order_id=header.id,
            source_ref="fixture://asn/dup-code",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_asn_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM asn WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_asn_organization_id" in joined
        or "uq_asn_org_id" in joined
        or "uq_asn_org_source_ref" in joined
        or "uq_asn_org_header_code" in joined
        or "Index Scan" in joined
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_asn_rejects_foreign_header(session, two_tenants) -> None:
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
        await AsnService(session).persist_asn(
            organization_id=org_a.id,
            user_id=user_a.id,
            purchase_order_id=header_b.id,
            asn_code="asn_01",
            plant_label=None,
            carrier_label=None,
            ship_ref_label=None,
            source_ref="fixture://asn/cross",
        )
