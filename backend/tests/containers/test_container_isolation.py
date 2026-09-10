from datetime import UTC, datetime
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_seal_no_3_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/s3",
            seal_no_3="XY1",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].seal_no_3 == "XY1"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_vessel_name_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/v1",
            vessel_name="MSC GULSUN",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].vessel_name == "MSC GULSUN"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_voyage_no_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/v2",
            voyage_no="049W",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].voyage_no == "049W"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_remarks_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/r1",
            remarks="keep dry",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].remarks == "keep dry"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_cargo_description_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/c1",
            cargo_description="steel coils",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].cargo_description == "steel coils"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_packaging_code_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/p1",
            packaging_code="CT",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].packaging_code == "CT"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_ref_1_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/m1",
            ref_1="PO123",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].ref_1 == "PO123"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_ref_2_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/m2",
            ref_2="BL456",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].ref_2 == "BL456"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_ref_3_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/m3",
            ref_3="PO789",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].ref_3 == "PO789"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_ref_4_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/m4",
            ref_4="BK012",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].ref_4 == "BK012"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_ref_5_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/m5",
            ref_5="SI345",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].ref_5 == "SI345"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_reefer_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/cold",
            reefer=True,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].reefer is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_pickup_terminal_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/dock",
            pickup_terminal="GCT",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].pickup_terminal == "GCT"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_return_terminal_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/yard",
            return_terminal="ECT",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].return_terminal == "ECT"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_bl_kind_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/bill",
            bl_kind="original",
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].bl_kind == "original"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_free_time_origin_h_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/idle",
            free_time_origin_h=48,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].free_time_origin_h == 48


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_free_time_dest_h_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/dwell",
            free_time_dest_h=24,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].free_time_dest_h == 24


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_si_cutoff_at_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    clock = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/si",
            si_cutoff_at=clock,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].si_cutoff_at == clock


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_ams_cutoff_at_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    clock = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/ams",
            ams_cutoff_at=clock,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].ams_cutoff_at == clock


@pytest.mark.integration
@pytest.mark.asyncio
async def test_container_cy_cutoff_at_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    clock = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)
    session.add(
        Container(
            id=uuid4(),
            organization_id=org_a.id,
            container_no="CSQU3054383",
            iso_size_type="22G1",
            source_ref="fixture://container/cy",
            cy_cutoff_at=clock,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Container))).all())
    assert loaded[0].cy_cutoff_at == clock
