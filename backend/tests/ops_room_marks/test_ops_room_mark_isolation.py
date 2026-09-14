from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.ops_room_mark import OpsRoomMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "ops_shift_01",
    layer_kind: str = "shift",
    source_ref: str = "tenant:manual",
) -> OpsRoomMark:
    return OpsRoomMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        layer_kind=layer_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ops_room_mark_rls_isolates_tenants(
    session,
    two_tenants,
) -> None:
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
        mark_code="ops_board_02",
        layer_kind="board",
        source_ref="fixture://ops-room-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(OpsRoomMark))).all())
    assert {row.id for row in visible_a} == {row_a.id}

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(OpsRoomMark))).all())
    assert {row.id for row in visible_b} == {row_b.id}
