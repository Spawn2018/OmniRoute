from datetime import time
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.terminal_slot_connector import TerminalSlotConnector


def _row(
    *,
    organization_id,
    created_by,
    connector_code: str = "gdynia_bct",
    terminal_code: str = "plgdy_bct",
    mode: str = "email_hitl",
    source_ref: str = "tenant:manual",
) -> TerminalSlotConnector:
    return TerminalSlotConnector(
        id=uuid4(),
        organization_id=organization_id,
        connector_code=connector_code,
        terminal_code=terminal_code,
        mode=mode,
        opens_local=time(6, 0),
        closes_local=time(22, 0),
        cutoff_local=time(16, 0),
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_slot_connector_rls_isolates_tenants(session, two_tenants) -> None:
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
        connector_code="szczecin_db",
        terminal_code="plszz_db",
        source_ref="fixture://terminal-slot-connector/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(TerminalSlotConnector))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(TerminalSlotConnector).where(TerminalSlotConnector.id == row_b.id)
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(TerminalSlotConnector))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_slot_connector_rejects_duplicate_source_ref(
    session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            connector_code="gdynia_gtc",
            terminal_code="plgdy_gtc",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_slot_connector_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            terminal_code="plgdy_gtc",
            source_ref="fixture://terminal-slot-connector/dup-code",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_slot_connector_rejects_duplicate_terminal(
    session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            connector_code="gdynia_gtc",
            source_ref="fixture://terminal-slot-connector/dup-term",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_slot_connector_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM terminal_slot_connector WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_terminal_slot_connector_organization_id" in joined
        or "uq_terminal_slot_connector_org_id" in joined
        or "uq_terminal_slot_connector_org_source_ref" in joined
        or "uq_terminal_slot_connector_org_code" in joined
        or "uq_terminal_slot_connector_org_terminal" in joined
        or "Index Scan" in joined
    )
