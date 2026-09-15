from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.data_source import DataSource


def _row(
    *,
    organization_id,
    created_by,
    source_code: str = "ds_openmeteo_01",
    license_label: str = "CC-BY-4.0",
    rights_scope: str = "weather read-only",
    source_ref: str = "tenant:manual",
) -> DataSource:
    return DataSource(
        id=uuid4(),
        organization_id=organization_id,
        source_code=source_code,
        license_label=license_label,
        rights_scope=rights_scope,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_data_source_rls_isolates_tenants(
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
        source_code="ds_nbp_02",
        license_label="public domain",
        rights_scope="fx table A",
        source_ref="fixture://data-source/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(DataSource))).all())
    assert {row.id for row in visible_a} == {row_a.id}

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(DataSource))).all())
    assert {row.id for row in visible_b} == {row_b.id}
