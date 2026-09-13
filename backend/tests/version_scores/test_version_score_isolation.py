from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.outcome_kind import OutcomeKind
from app.models.outcome_ledger import OutcomeLedger
from app.models.suggestion_kind import SuggestionKind
from app.models.suggestion_ledger import SuggestionLedger
from app.models.version_score import VersionScore


def _seed_pair(
    session,
    *,
    organization_id,
    created_by,
    kind_code: str,
    tag: str,
) -> None:
    session.add(
        SuggestionKind(
            id=uuid4(),
            organization_id=organization_id,
            kind_code=kind_code,
            source_ref=f"fixture://suggestion-kind/{tag}",
            created_by=created_by,
        )
    )
    session.add(
        OutcomeKind(
            id=uuid4(),
            organization_id=organization_id,
            kind_code=kind_code,
            source_ref=f"fixture://outcome-kind/{tag}",
            created_by=created_by,
        )
    )


async def _flush_pair(
    session,
    *,
    organization_id,
    created_by,
    kind_code: str,
    low: str,
    high: str,
    actual: str,
    tag: str,
) -> None:
    suggestion = SuggestionLedger(
        id=uuid4(),
        organization_id=organization_id,
        target_bc="shipment",
        entity_id=uuid4(),
        suggestion_kind=kind_code,
        interval_low=Decimal(low),
        interval_high=Decimal(high),
        model_version="hist_eta",
        prompt_version="prompt_v1",
        reaction="accept",
        changed_to="none",
        source_ref=f"fixture://suggestion-ledger/{tag}",
        created_by=created_by,
    )
    session.add(suggestion)
    await session.flush()
    session.add(
        OutcomeLedger(
            id=uuid4(),
            organization_id=organization_id,
            target_bc="shipment",
            entity_id=suggestion.entity_id,
            suggestion_id=suggestion.id,
            outcome_kind=kind_code,
            actual_value=Decimal(actual),
            source_ref=f"fixture://outcome-ledger/{tag}",
            created_by=created_by,
        )
    )
    await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_version_score_averages_two_pairs(session, two_tenants) -> None:
    org = two_tenants["org_a"]
    user = two_tenants["user_a"]
    await bind_tenant(session, org.id)
    _seed_pair(
        session,
        organization_id=org.id,
        created_by=user.id,
        kind_code="eta",
        tag="a-avg",
    )
    await session.flush()
    await _flush_pair(
        session,
        organization_id=org.id,
        created_by=user.id,
        kind_code="eta",
        low="0",
        high="6",
        actual="3",
        tag="a-avg-1",
    )
    await _flush_pair(
        session,
        organization_id=org.id,
        created_by=user.id,
        kind_code="eta",
        low="10",
        high="10",
        actual="12",
        tag="a-avg-2",
    )
    rows = list((await session.scalars(select(VersionScore))).all())
    assert len(rows) == 1
    assert rows[0].pair_count == 2
    assert rows[0].avg_mae == Decimal("1.0000")
    assert rows[0].avg_crps == Decimal("1.2500")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_version_score_view_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    _seed_pair(
        session,
        organization_id=org_a.id,
        created_by=user_a.id,
        kind_code="eta",
        tag="a-iso",
    )
    await session.flush()
    await _flush_pair(
        session,
        organization_id=org_a.id,
        created_by=user_a.id,
        kind_code="eta",
        low="0",
        high="6",
        actual="3",
        tag="a-iso",
    )

    await bind_tenant(session, org_b.id)
    _seed_pair(
        session,
        organization_id=org_b.id,
        created_by=user_b.id,
        kind_code="rate",
        tag="b-iso",
    )
    await session.flush()
    await _flush_pair(
        session,
        organization_id=org_b.id,
        created_by=user_b.id,
        kind_code="rate",
        low="10",
        high="20",
        actual="15",
        tag="b-iso",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(VersionScore))).all())
    assert len(visible) == 1
    assert visible[0].organization_id == org_a.id
    assert visible[0].pair_count == 1
