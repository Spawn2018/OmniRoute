from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.resource import Resource
from app.models.resource_document import ResourceDocument


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resource_document_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    fleet_a = Resource(
        id=uuid4(),
        organization_id=org_a.id,
        resource_kind="vehicle",
        display_name="MAN A",
        source_ref="fixture://resource/doc-a",
        created_by=user_a.id,
    )
    session.add(fleet_a)
    await session.flush()
    doc_a = ResourceDocument(
        id=uuid4(),
        organization_id=org_a.id,
        resource_id=fleet_a.id,
        document_kind="licence",
        valid_until=date(2027, 1, 1),
        source_ref="fixture://resource-document/a",
        created_by=user_a.id,
    )
    session.add(doc_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    fleet_b = Resource(
        id=uuid4(),
        organization_id=org_b.id,
        resource_kind="driver",
        display_name="Kowalski",
        source_ref="fixture://resource/doc-b",
        created_by=user_b.id,
    )
    session.add(fleet_b)
    await session.flush()
    doc_b = ResourceDocument(
        id=uuid4(),
        organization_id=org_b.id,
        resource_id=fleet_b.id,
        document_kind="insurance",
        valid_until=date(2027, 2, 1),
        source_ref="fixture://resource-document/b",
        created_by=user_b.id,
    )
    session.add(doc_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(ResourceDocument))).all())
    assert {row.id for row in visible} == {doc_a.id}
    assert await session.get(ResourceDocument, doc_b.id) is None
