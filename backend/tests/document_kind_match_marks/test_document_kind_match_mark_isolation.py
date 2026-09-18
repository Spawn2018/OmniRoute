from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.document_kind_match_mark import DocumentKindMatchMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "match_01",
    match_kind: str = "exact",
    source_ref: str = "tenant:manual",
) -> DocumentKindMatchMark:
    return DocumentKindMatchMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        match_kind=match_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_document_kind_match_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="match_02",
        match_kind="alias",
        source_ref="fixture://document-kind-match-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(DocumentKindMatchMark))).all())
    assert {row.id for row in visible} == {row_a.id}
