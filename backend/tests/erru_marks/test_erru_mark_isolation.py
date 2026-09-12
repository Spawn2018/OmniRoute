from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.erru_mark import ErruMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "erm_to_verify_01",
    check_kind: str = "to_verify",
    source_ref: str = "fixture://erru-mark/",
) -> ErruMark:
    return ErruMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        check_kind=check_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_erru_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="erm_clear_01",
        check_kind="clear",
        source_ref="fixture://erru-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(ErruMark))).all())
    assert {row.id for row in visible} == {row_a.id}
