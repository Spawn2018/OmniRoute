from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.domain.errors import InvalidSourceRef
from app.models.port import Port
from app.services.geography.unlocode_ingest import ingest_ports
from tests.geography.unlocode_fixture import FIXTURE_SOURCE_REF, sample_records

_BACKEND = Path(__file__).resolve().parents[2]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ingest_writes_every_fixture_record_for_the_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    records = sample_records()

    await bind_tenant(session, org_a.id)
    await ingest_ports(
        session,
        organization_id=org_a.id,
        records=records,
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()

    rows = list((await session.scalars(select(Port))).all())
    assert {row.unlocode for row in rows} == {"PLGDY", "PLGDN", "PLSZZ", "DEHAM", "PLWAW"}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_repeated_ingest_of_the_same_source_creates_no_duplicates(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    records = sample_records()

    await bind_tenant(session, org_a.id)
    for _ in range(2):
        await ingest_ports(
            session,
            organization_id=org_a.id,
            records=records,
            source_ref=FIXTURE_SOURCE_REF,
        )
    await session.flush()

    rows = list((await session.scalars(select(Port))).all())
    assert len(rows) == len(records)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reingest_updates_the_existing_row_instead_of_inserting(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    records = sample_records()

    await bind_tenant(session, org_a.id)
    await ingest_ports(
        session,
        organization_id=org_a.id,
        records=records,
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()
    original = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert original is not None
    original_id = original.id

    renamed = [
        replace(record, name="Gdynia Port") if record.unlocode == "PLGDY" else record
        for record in records
    ]
    await ingest_ports(
        session,
        organization_id=org_a.id,
        records=renamed,
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()
    session.expunge_all()

    await bind_tenant(session, org_a.id)
    updated = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert updated is not None
    assert updated.id == original_id
    assert updated.name == "Gdynia Port"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_every_ingested_row_carries_the_source_pin(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    await ingest_ports(
        session,
        organization_id=org_a.id,
        records=sample_records(),
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()

    rows = list((await session.scalars(select(Port))).all())
    assert {row.source_ref for row in rows} == {FIXTURE_SOURCE_REF}
    assert all(row.is_official for row in rows)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ingest_rejects_batch_without_source_pin(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    with pytest.raises(InvalidSourceRef):
        await ingest_ports(
            session,
            organization_id=org_a.id,
            records=sample_records(),
            source_ref="   ",
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ingest_decodes_functions_and_stores_decimal_coordinates(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    await ingest_ports(
        session,
        organization_id=org_a.id,
        records=sample_records(),
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()

    gdynia = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert gdynia is not None
    assert gdynia.is_seaport is True
    assert gdynia.function_flags == ["port", "rail", "airport", "icd"]
    assert isinstance(gdynia.lat, Decimal)
    assert gdynia.lat == Decimal("54.516667")

    warszawa = await session.scalar(select(Port).where(Port.unlocode == "PLWAW"))
    assert warszawa is not None
    assert warszawa.is_seaport is False
    assert warszawa.lat is None


def test_ports_endpoint_never_fetches_the_upstream_source() -> None:
    endpoint = (_BACKEND / "app" / "api" / "ports.py").read_text(encoding="utf-8")
    assert "github" not in endpoint.lower()
    assert "httpx" not in endpoint
    assert "urllib" not in endpoint
