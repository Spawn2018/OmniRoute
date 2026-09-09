from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.container import Container
from tests.sales_invoices.test_sales_invoice_isolation import _booked


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = Container(
        id=uuid4(),
        organization_id=org_a.id,
        container_no="CSQU3054383",
        iso_size_type="22G1",
        source_ref="fixture://container/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = Container(
        id=uuid4(),
        organization_id=org_b.id,
        container_no="CSQU3054383",
        iso_size_type="45G1",
        source_ref="fixture://container/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Container))).all())
    assert {row.iso_size_type for row in visible_a} == {"22G1"}
    assert await session.scalar(select(Container).where(Container.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Container))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="cx")
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            shipment_id=ship_b.id,
            source_ref="fixture://container/x",
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_list_uses_org_type_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM container "
            "WHERE organization_id = :org_id AND iso_size_type = '22G1' "
            "AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_container_org_type" in joined


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_seal_no_1_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/s1",
            seal_no_1="MSC1234567",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].seal_no_1 == "MSC1234567"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_seal_no_2_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/s2",
            seal_no_2="HL987",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].seal_no_2 == "HL987"
