from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.carbon_method import CarbonMethod


def _method(
    *,
    organization_id,
    created_by,
    method_code: str = "glec",
    method_version: str = "2023",
) -> CarbonMethod:
    return CarbonMethod(
        id=uuid4(),
        organization_id=organization_id,
        method_code=method_code,
        method_version=method_version,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carbon_method_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _method(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _method(
        organization_id=org_b.id,
        created_by=user_b.id,
        method_code="ghg_protocol",
        method_version="v3",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CarbonMethod))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(CarbonMethod).where(CarbonMethod.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CarbonMethod))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carbon_method_rejects_duplicate_code_version(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_method(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_method(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carbon_method_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM carbon_method WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_carbon_method_organization_id" in joined
        or "uq_carbon_method_org_code_version" in joined
    )
