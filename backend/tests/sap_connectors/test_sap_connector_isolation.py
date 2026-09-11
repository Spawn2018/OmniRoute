from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.sap_connector import SapConnector


def _row(
    *,
    organization_id,
    created_by,
    connector_code: str = "sap_pl_01",
    source_ref: str = "tenant:manual",
) -> SapConnector:
    return SapConnector(
        id=uuid4(),
        organization_id=organization_id,
        connector_code=connector_code,
        system_kind="sap",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sap_connector_rls_isolates_tenants(session, two_tenants) -> None:
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
        connector_code="oracle_de_01",
        source_ref="fixture://sap-connector/b",
    )
    row_b.system_kind = "oracle"
    session.add(row_b)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(SapConnector))).all())
    assert {row.id for row in visible} == {row_a.id}
    hidden = await session.scalar(select(SapConnector).where(SapConnector.id == row_b.id))
    assert hidden is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sap_connector_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_row(organization_id=org_a.id, created_by=user_a.id, connector_code="sap_02"))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sap_connector_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM sap_connector WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_sap_connector_organization_id" in joined
        or "uq_sap_connector_org_id" in joined
        or "uq_sap_connector_org_source_ref" in joined
        or "uq_sap_connector_org_code" in joined
        or "Index Scan" in joined
    )
