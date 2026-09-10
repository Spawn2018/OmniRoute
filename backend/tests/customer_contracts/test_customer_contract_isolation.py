from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.customer_contract import CustomerContract


def _row(
    *,
    organization_id,
    created_by,
    contract_code: str = "acme_pl_2026",
    shipper_label: str = "Acme Logistics",
    their_customer_label: str = "Bayer PL",
    source_ref: str = "tenant:manual",
    blob_ciphertext: bytes | None = None,
) -> CustomerContract:
    return CustomerContract(
        id=uuid4(),
        organization_id=organization_id,
        contract_code=contract_code,
        shipper_label=shipper_label,
        their_customer_label=their_customer_label,
        source_ref=source_ref,
        blob_ciphertext=blob_ciphertext,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_contract_rls_isolates_tenants(session, two_tenants) -> None:
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
        contract_code="beta_de_2026",
        source_ref="fixture://contract/b",
        blob_ciphertext=b"tenant-b-opaque-fixture",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CustomerContract))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    hidden = select(CustomerContract).where(CustomerContract.id == row_b.id)
    assert await session.scalar(hidden) is None
    leaked = await session.execute(
        text("SELECT blob_ciphertext FROM customer_contract WHERE id = :row_id"),
        {"row_id": row_b.id},
    )
    assert leaked.first() is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CustomerContract))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_contract_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            contract_code="acme_pl_other",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_contract_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            source_ref="fixture://contract/dup-code",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_contract_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM customer_contract WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_customer_contract_organization_id" in joined
        or "uq_customer_contract_org_id" in joined
        or "uq_customer_contract_org_source_ref" in joined
        or "uq_customer_contract_org_code" in joined
        or "Index Scan" in joined
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_contract_stores_fixture_bytes_under_rls(
    session,
    two_tenants,
) -> None:
    from app.domain.customer_contract import fixture_opaque_blob
    from app.services.customer_contracts.customer_contract_service import (
        CustomerContractService,
    )

    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    stored = await CustomerContractService(session).persist_customer_contract(
        organization_id=org_a.id,
        user_id=user_a.id,
        contract_code="acme_pl_2026",
        shipper_label="Acme Logistics",
        their_customer_label="Bayer PL",
        source_ref="fixture://contract/opaque-1",
        opaque_fixture=True,
        opaque_blob=None,
    )
    assert stored.blob_ciphertext == fixture_opaque_blob()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    reloaded = await session.get(CustomerContract, stored.id)
    assert reloaded is not None
    assert reloaded.blob_ciphertext == fixture_opaque_blob()
