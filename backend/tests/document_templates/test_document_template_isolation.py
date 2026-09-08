from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.document_template import DocumentTemplate

_MANUAL = "tenant:manual"


def _sheet(*, organization_id, created_by, kind: str, layout: str):
    return DocumentTemplate(
        id=uuid4(),
        organization_id=organization_id,
        template_kind=kind,
        language="pl",
        layout_ref=layout,
        output_kind="html_print",
        source_ref=_MANUAL,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_document_template_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _sheet(
        organization_id=org_a.id,
        created_by=user_a.id,
        kind="own_label",
        layout="own-label-pl",
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _sheet(
        organization_id=org_b.id,
        created_by=user_b.id,
        kind="cmr",
        layout="cmr-pl",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(DocumentTemplate))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(DocumentTemplate).where(DocumentTemplate.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(DocumentTemplate))).all())
    assert {row.id for row in visible_b} == {row_b.id}
