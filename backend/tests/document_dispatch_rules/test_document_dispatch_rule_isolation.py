from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.core.database import bind_tenant
from app.models.document_dispatch_rule import DocumentDispatchRule


@pytest.mark.integration
@pytest.mark.asyncio
async def test_document_dispatch_rule_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = DocumentDispatchRule(
        id=uuid4(),
        organization_id=org_a.id,
        incoterm="DAP",
        trade_side="import",
        document_kind="commercial_invoice",
        recipient_role="omni_customs",
        source_ref="fixture://document-dispatch-rule/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = DocumentDispatchRule(
        id=uuid4(),
        organization_id=org_b.id,
        incoterm="FOB",
        trade_side="export",
        document_kind="bill_of_lading",
        recipient_role="origin_agent",
        source_ref="fixture://document-dispatch-rule/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(DocumentDispatchRule))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(DocumentDispatchRule).where(DocumentDispatchRule.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(DocumentDispatchRule))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_document_dispatch_rule_list_uses_org_triple_index(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM document_dispatch_rule "
            "WHERE organization_id = :org_id AND incoterm = 'DAP' "
            "AND trade_side = 'import' AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_document_dispatch_rule_org_triple" in joined
