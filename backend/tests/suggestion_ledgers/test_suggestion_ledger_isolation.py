from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.suggestion_ledger import SuggestionLedger

_ENTITY_A = uuid4()
_ENTITY_B = uuid4()


def _row(
    *,
    organization_id,
    created_by,
    source_ref: str = "fixture://suggestion-ledger/",
    suggestion_kind: str = "eta",
    reaction: str = "accept",
    changed_to: str = "none",
) -> SuggestionLedger:
    return SuggestionLedger(
        id=uuid4(),
        organization_id=organization_id,
        target_bc="shipment",
        entity_id=_ENTITY_A if source_ref.endswith("/") else _ENTITY_B,
        suggestion_kind=suggestion_kind,
        interval_low=Decimal("30"),
        interval_high=Decimal("90"),
        model_version="hist_eta",
        prompt_version="prompt_v1",
        reaction=reaction,
        changed_to=changed_to,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_suggestion_ledger_rls_isolates_tenants(session, two_tenants) -> None:
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
        suggestion_kind="rate",
        source_ref="fixture://suggestion-ledger/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(SuggestionLedger))).all())
    assert {row.id for row in visible} == {row_a.id}
