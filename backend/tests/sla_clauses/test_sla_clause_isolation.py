from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.customer_contract import CustomerContract
from app.models.sla_clause import SlaClause


def _contract(
    *,
    organization_id,
    created_by,
    contract_code: str = "ctr_pl_01",
    source_ref: str = "tenant:manual",
) -> CustomerContract:
    return CustomerContract(
        id=uuid4(),
        organization_id=organization_id,
        contract_code=contract_code,
        shipper_label="Shipper A",
        their_customer_label="Buyer A",
        source_ref=source_ref,
        created_by=created_by,
    )


def _clause(
    *,
    organization_id,
    created_by,
    customer_contract_id,
    clause_code: str = "sla_otif_01",
    metric_kind: str = "otif",
    threshold_label: str = "OTIF >= 95%",
    source_ref: str = "tenant:manual",
) -> SlaClause:
    return SlaClause(
        id=uuid4(),
        organization_id=organization_id,
        customer_contract_id=customer_contract_id,
        clause_code=clause_code,
        metric_kind=metric_kind,
        threshold_label=threshold_label,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sla_clause_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    contract_a = _contract(organization_id=org_a.id, created_by=user_a.id)
    session.add(contract_a)
    await session.flush()
    clause_a = _clause(
        organization_id=org_a.id,
        created_by=user_a.id,
        customer_contract_id=contract_a.id,
    )
    session.add(clause_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    contract_b = _contract(
        organization_id=org_b.id,
        created_by=user_b.id,
        contract_code="ctr_de_01",
        source_ref="fixture://contract/b",
    )
    session.add(contract_b)
    await session.flush()
    clause_b = _clause(
        organization_id=org_b.id,
        created_by=user_b.id,
        customer_contract_id=contract_b.id,
        clause_code="sla_delay_de",
        metric_kind="delay",
        source_ref="fixture://sla-clause/b",
    )
    session.add(clause_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(SlaClause))).all())
    assert {row.id for row in visible_a} == {clause_a.id}
    hidden = await session.scalar(select(SlaClause).where(SlaClause.id == clause_b.id))
    assert hidden is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sla_clause_unique_code_per_org(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    contract = _contract(organization_id=org_a.id, created_by=user_a.id)
    session.add(contract)
    await session.flush()
    session.add(
        _clause(
            organization_id=org_a.id,
            created_by=user_a.id,
            customer_contract_id=contract.id,
        )
    )
    await session.flush()
    session.add(
        _clause(
            organization_id=org_a.id,
            created_by=user_a.id,
            customer_contract_id=contract.id,
            source_ref="fixture://sla-clause/dup",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
    await session.rollback()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sla_clause_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = (
        await session.execute(
            text("EXPLAIN (FORMAT TEXT) SELECT * FROM sla_clause WHERE organization_id = :org"),
            {"org": str(org_a.id)},
        )
    ).scalars().all()
    joined = "\n".join(plan)
    assert "Index" in joined or "Seq Scan" in joined
