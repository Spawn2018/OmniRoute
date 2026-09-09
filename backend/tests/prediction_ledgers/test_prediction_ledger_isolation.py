from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.prediction_ledger import PredictionLedger


def _row(
    *,
    organization_id,
    created_by,
    source_ref: str = "tenant:manual",
    model_code: str = "hist_eta",
) -> PredictionLedger:
    return PredictionLedger(
        id=uuid4(),
        organization_id=organization_id,
        prediction_kind="eta",
        horizon_code="h24h",
        interval_low=Decimal("30"),
        interval_high=Decimal("90"),
        crps=Decimal("0.25"),
        mae=Decimal("12"),
        model_code=model_code,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_prediction_ledger_rls_isolates_tenants(session, two_tenants) -> None:
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
        source_ref="fixture://prediction-ledger/b",
        model_code="ais_eta",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PredictionLedger))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert (
        await session.scalar(select(PredictionLedger).where(PredictionLedger.id == row_b.id))
        is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PredictionLedger))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_prediction_ledger_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_row(organization_id=org_a.id, created_by=user_a.id, model_code="ais_eta"))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_prediction_ledger_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM prediction_ledger WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_prediction_ledger_organization_id" in joined
        or "uq_prediction_ledger_org_source_ref" in joined
    )
