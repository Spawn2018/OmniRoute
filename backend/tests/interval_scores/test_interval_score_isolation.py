from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.core.database import bind_tenant
from app.models.interval_score import IntervalScore
from app.models.outcome_kind import OutcomeKind
from app.models.outcome_ledger import OutcomeLedger
from app.models.suggestion_kind import SuggestionKind
from app.models.suggestion_ledger import SuggestionLedger


def _suggestion_kind(
    *,
    organization_id,
    created_by,
    kind_code: str,
    source_ref: str,
) -> SuggestionKind:
    return SuggestionKind(
        id=uuid4(),
        organization_id=organization_id,
        kind_code=kind_code,
        source_ref=source_ref,
        created_by=created_by,
    )


def _outcome_kind(*, organization_id, created_by, kind_code: str, source_ref: str) -> OutcomeKind:
    return OutcomeKind(
        id=uuid4(),
        organization_id=organization_id,
        kind_code=kind_code,
        source_ref=source_ref,
        created_by=created_by,
    )


def _suggestion(
    *,
    organization_id,
    created_by,
    suggestion_kind: str,
    source_ref: str,
    low: str,
    high: str,
) -> SuggestionLedger:
    return SuggestionLedger(
        id=uuid4(),
        organization_id=organization_id,
        target_bc="shipment",
        entity_id=uuid4(),
        suggestion_kind=suggestion_kind,
        interval_low=Decimal(low),
        interval_high=Decimal(high),
        model_version="hist_eta",
        prompt_version="prompt_v1",
        reaction="accept",
        changed_to="none",
        source_ref=source_ref,
        created_by=created_by,
    )


def _outcome(
    *,
    organization_id,
    created_by,
    suggestion_id,
    entity_id,
    outcome_kind: str,
    source_ref: str,
    actual: str,
) -> OutcomeLedger:
    return OutcomeLedger(
        id=uuid4(),
        organization_id=organization_id,
        target_bc="shipment",
        entity_id=entity_id,
        suggestion_id=suggestion_id,
        outcome_kind=outcome_kind,
        actual_value=Decimal(actual),
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_interval_sql_pins_uniform_crps_and_midpoint_mae(session, two_tenants) -> None:
    await bind_tenant(session, two_tenants["org_a"].id)
    mae = (
        await session.execute(text("SELECT interval_mae(0, 6, 3)"))
    ).scalar_one()
    crps = (
        await session.execute(text("SELECT interval_crps(0, 6, 3)"))
    ).scalar_one()
    point = (
        await session.execute(text("SELECT interval_crps(10, 10, 12)"))
    ).scalar_one()
    assert mae == Decimal("0.0000")
    assert crps == Decimal("0.5000")
    assert point == Decimal("2.0000")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_interval_score_view_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    session.add(
        _suggestion_kind(
            organization_id=org_a.id,
            created_by=user_a.id,
            kind_code="eta",
            source_ref="fixture://suggestion-kind/a-eta-score",
        )
    )
    session.add(
        _outcome_kind(
            organization_id=org_a.id,
            created_by=user_a.id,
            kind_code="eta",
            source_ref="fixture://outcome-kind/a-eta-score",
        )
    )
    await session.flush()
    suggestion_a = _suggestion(
        organization_id=org_a.id,
        created_by=user_a.id,
        suggestion_kind="eta",
        source_ref="fixture://suggestion-ledger/a-score",
        low="0",
        high="6",
    )
    session.add(suggestion_a)
    await session.flush()
    outcome_a = _outcome(
        organization_id=org_a.id,
        created_by=user_a.id,
        suggestion_id=suggestion_a.id,
        entity_id=suggestion_a.entity_id,
        outcome_kind="eta",
        source_ref="fixture://outcome-ledger/a-score",
        actual="3",
    )
    session.add(outcome_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(
        _suggestion_kind(
            organization_id=org_b.id,
            created_by=user_b.id,
            kind_code="rate",
            source_ref="fixture://suggestion-kind/b-rate-score",
        )
    )
    session.add(
        _outcome_kind(
            organization_id=org_b.id,
            created_by=user_b.id,
            kind_code="rate",
            source_ref="fixture://outcome-kind/b-rate-score",
        )
    )
    await session.flush()
    suggestion_b = _suggestion(
        organization_id=org_b.id,
        created_by=user_b.id,
        suggestion_kind="rate",
        source_ref="fixture://suggestion-ledger/b-score",
        low="10",
        high="20",
    )
    session.add(suggestion_b)
    await session.flush()
    session.add(
        _outcome(
            organization_id=org_b.id,
            created_by=user_b.id,
            suggestion_id=suggestion_b.id,
            entity_id=suggestion_b.entity_id,
            outcome_kind="rate",
            source_ref="fixture://outcome-ledger/b-score",
            actual="15",
        )
    )
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(IntervalScore))).all())
    assert {row.outcome_id for row in visible} == {outcome_a.id}
    assert visible[0].mae == Decimal("0.0000")
    assert visible[0].crps == Decimal("0.5000")
