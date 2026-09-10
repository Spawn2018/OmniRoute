from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.exchange_connector import ExchangeConnector


def _row(
    *,
    organization_id,
    created_by,
    connector_code: str = "trans_eu_desk",
    system_kind: str = "trans_eu",
    source_ref: str = "tenant:manual",
) -> ExchangeConnector:
    return ExchangeConnector(
        id=uuid4(),
        organization_id=organization_id,
        connector_code=connector_code,
        system_kind=system_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_exchange_connector_rls_isolates_tenants(session, two_tenants) -> None:
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
        connector_code="trans_eu_oddzial",
        source_ref="fixture://portal/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ExchangeConnector))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    hidden = select(ExchangeConnector).where(ExchangeConnector.id == row_b.id)
    assert await session.scalar(hidden) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ExchangeConnector))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_exchange_connector_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            connector_code="trans_eu_druga",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_exchange_connector_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            source_ref="fixture://portal/dup-code",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_exchange_connector_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM exchange_connector WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_exchange_connector_organization_id" in joined
        or "uq_exchange_connector_org_id" in joined
        or "uq_exchange_connector_org_source_ref" in joined
        or "uq_exchange_connector_org_code" in joined
        or "Index Scan" in joined
    )
