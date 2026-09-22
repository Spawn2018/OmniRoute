from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.pallet_synchro_mark import PalletSynchroMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "synchro_aligned_01",
    synchro_kind: str = "aligned",
    source_ref: str = "tenant:manual",
) -> PalletSynchroMark:
    return PalletSynchroMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        synchro_kind=synchro_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pallet_synchro_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="synchro_drift_b",
        synchro_kind="drift",
        source_ref="fixture://pallet-synchro/b",
    )
    session.add(row_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(PalletSynchroMark))).all())
    assert {row.mark_code for row in visible} == {"synchro_aligned_01"}
