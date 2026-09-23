from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.network_print_gate_mark import NetworkPrintGateMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "gate_block_01",
    gate_kind: str = "block_409",
    source_ref: str = "tenant:manual",
) -> NetworkPrintGateMark:
    return NetworkPrintGateMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        gate_kind=gate_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_network_print_gate_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="gate_warn_b",
        gate_kind="warn_only",
        source_ref="fixture://network-print-gate/b",
    )
    session.add(row_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(NetworkPrintGateMark))).all())
    assert {row.mark_code for row in visible} == {"gate_block_01"}
