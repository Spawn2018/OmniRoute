from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.weather_observation import WeatherObservation

_CLOCK = datetime(2026, 9, 9, 12, 0, tzinfo=UTC)


def _mark(
    *,
    organization_id,
    created_by,
    source_ref: str = "tenant:manual",
    condition_code: str = "rain",
) -> WeatherObservation:
    return WeatherObservation(
        id=uuid4(),
        organization_id=organization_id,
        condition_code=condition_code,
        station_unlocode="PLGDY",
        observed_at=_CLOCK,
        provider_code="hitl",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_weather_observation_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _mark(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _mark(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://weather-observation/b",
        condition_code="fog",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(WeatherObservation))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(WeatherObservation).where(WeatherObservation.id == row_b.id)
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(WeatherObservation))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_weather_observation_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_mark(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_mark(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_weather_observation_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'weather_observation' "
            "AND indexname = 'ix_weather_observation_organization_id'"
        ),
    )
    assert named.first() is not None
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM weather_observation WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_weather_observation_organization_id" in joined
        or "uq_weather_observation_org_source_ref" in joined
        or "Index Scan" in joined
    )
