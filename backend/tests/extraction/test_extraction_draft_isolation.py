from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.extraction_draft import ExtractionDraft


@pytest.mark.integration
@pytest.mark.asyncio
async def test_extraction_draft_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    draft_a = ExtractionDraft(
        id=uuid4(),
        organization_id=org_a.id,
        status="pending",
        source_ref="doc://a",
        input_text="THC 100 EUR",
        payload={"source_ref": "doc://a", "unparsed_regions": [], "candidates": []},
        created_by=user_a.id,
    )
    draft_b = ExtractionDraft(
        id=uuid4(),
        organization_id=org_b.id,
        status="pending",
        source_ref="doc://b",
        input_text="BAF 20 USD",
        payload={"source_ref": "doc://b", "unparsed_regions": [], "candidates": []},
        created_by=user_b.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(draft_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(draft_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ExtractionDraft))).all())
    assert {row.id for row in visible_a} == {draft_a.id}
    foreign_b = await session.scalar(
        select(ExtractionDraft).where(ExtractionDraft.id == draft_b.id),
    )
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ExtractionDraft))).all())
    assert {row.id for row in visible_b} == {draft_b.id}
    foreign_a = await session.scalar(
        select(ExtractionDraft).where(ExtractionDraft.id == draft_a.id),
    )
    assert foreign_a is None
