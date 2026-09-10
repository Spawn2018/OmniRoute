from uuid import UUID, uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.task_template import TaskTemplate


def _blueprint(
    *,
    organization_id: UUID,
    created_by: UUID,
    source_ref: str = "tenant:manual",
    template_code: str = "gate_in",
    applies_when: str = "container at CY",
) -> TaskTemplate:
    return TaskTemplate(
        id=uuid4(),
        organization_id=organization_id,
        template_code=template_code,
        applies_when=applies_when,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_template_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _blueprint(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _blueprint(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://task-template/b",
        template_code="vgm_cut",
        applies_when="vgm window open",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(TaskTemplate))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    hidden = select(TaskTemplate).where(TaskTemplate.id == row_b.id)
    assert await session.scalar(hidden) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(TaskTemplate))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_template_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_blueprint(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _blueprint(
            organization_id=org_a.id,
            created_by=user_a.id,
            template_code="si_cut",
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_template_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_blueprint(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _blueprint(
            organization_id=org_a.id,
            created_by=user_a.id,
            source_ref="fixture://task-template/dup-code",
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_template_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'task_template' "
            "AND indexname = 'ix_task_template_organization_id'"
        ),
    )
    assert named.first() is not None
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM task_template WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_task_template_organization_id" in joined
        or "uq_task_template_org_code" in joined
        or "Index Scan" in joined
    )
