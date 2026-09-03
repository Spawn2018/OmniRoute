from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.fraud_flag import FraudFlag
from app.models.party import Party

_MANUAL = "tenant:manual"


def _party(*, organization_id, legal_name: str, created_by):
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["agent"],
        source_ref=_MANUAL,
        is_active=True,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fraud_flag_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Agent A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    row_a = FraudFlag(
        id=uuid4(),
        organization_id=org_a.id,
        party_id=party_a.id,
        flag_kind="billing",
        source_ref="fixture://fraud-flag/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Agent B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    row_b = FraudFlag(
        id=uuid4(),
        organization_id=org_b.id,
        party_id=party_b.id,
        flag_kind="document",
        source_ref="fixture://fraud-flag/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(FraudFlag))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(FraudFlag).where(FraudFlag.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(FraudFlag))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fraud_flag_rejects_foreign_party(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Agent X", created_by=user_b.id)
    session.add(party_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        FraudFlag(
            id=uuid4(),
            organization_id=org_a.id,
            party_id=party_b.id,
            flag_kind="other",
            source_ref="fixture://fraud-flag/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
