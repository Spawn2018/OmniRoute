from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.monitoring_scheme import MonitoringScheme


def _scheme(
    *,
    organization_id,
    created_by,
    scheme_code: str = "sent",
) -> MonitoringScheme:
    return MonitoringScheme(
        id=uuid4(),
        organization_id=organization_id,
        scheme_code=scheme_code,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_monitoring_scheme_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _scheme(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _scheme(
        organization_id=org_b.id,
        created_by=user_b.id,
        scheme_code="ekaer",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(MonitoringScheme))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert (
        await session.scalar(select(MonitoringScheme).where(MonitoringScheme.id == row_b.id))
        is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(MonitoringScheme))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_monitoring_scheme_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_scheme(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_scheme(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_monitoring_scheme_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM monitoring_scheme WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_monitoring_scheme_organization_id" in joined
        or "uq_monitoring_scheme_org_code" in joined
    )
