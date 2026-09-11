from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.subcontract_edge_mark import SubcontractEdgeMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "prime_01",
    edge_kind: str = "prime",
    source_ref: str = "tenant:manual",
) -> SubcontractEdgeMark:
    return SubcontractEdgeMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        edge_kind=edge_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_subcontract_edge_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="shared_01",
        edge_kind="broker",
        source_ref="fixture://subcontract-edge-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(SubcontractEdgeMark))).all())
    assert {row.id for row in visible} == {row_a.id}
