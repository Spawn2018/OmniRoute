from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.cod_instruction import CodInstruction
from tests.sales_invoices.test_sales_invoice_isolation import _booked


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cod_instruction_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="oa")
    row_a = CodInstruction(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        instruction_code="cod_west",
        collection_status="noted",
        source_ref="fixture://cod-instruction/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="ob")
    row_b = CodInstruction(
        id=uuid4(),
        organization_id=org_b.id,
        shipment_id=ship_b.id,
        instruction_code="cod_east",
        collection_status="advised",
        source_ref="fixture://cod-instruction/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CodInstruction))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(CodInstruction).where(CodInstruction.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CodInstruction))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cod_instruction_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="ox")

    await bind_tenant(session, org_a.id)
    session.add(
        CodInstruction(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            instruction_code="cod_stolen",
            collection_status="noted",
            source_ref="fixture://cod-instruction/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
