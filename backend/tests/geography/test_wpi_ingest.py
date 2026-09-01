from decimal import Decimal
from importlib import import_module
from pathlib import Path

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.port import Port
from app.services.geography.unlocode_ingest import ingest_ports
from tests.geography.unlocode_fixture import FIXTURE_SOURCE_REF, sample_records
from tests.geography.wpi_fixture import FIXTURE_SOURCE_REF as WPI_SOURCE_REF
from tests.geography.wpi_fixture import sample_csv

_BACKEND = Path(__file__).resolve().parents[2]
_WPI_COLUMNS = (
    "wpi_number",
    "harbor_size",
    "harbor_type",
    "shelter",
    "channel_depth_m",
    "cargo_pier_depth_m",
    "wpi_source_ref",
)


async def _seed_ports(session, organization_id) -> None:
    await bind_tenant(session, organization_id)
    await ingest_ports(
        session,
        organization_id=organization_id,
        records=sample_records(),
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()


def test_port_table_carries_world_port_index_columns() -> None:
    for column in _WPI_COLUMNS:
        assert column in Port.__table__.c


def test_port_response_exposes_world_port_index_fields() -> None:
    from app.api.ports import PortResponse

    for column in _WPI_COLUMNS:
        assert column in PortResponse.model_fields


def test_wpi_depths_are_numeric_not_float() -> None:
    channel = Port.__table__.c.channel_depth_m
    cargo = Port.__table__.c.cargo_pier_depth_m
    assert str(channel.type).lower().startswith("numeric")
    assert str(cargo.type).lower().startswith("numeric")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ingest_assigns_wpi_number_to_fixture_gdynia(session, two_tenants) -> None:
    wpi = import_module("app.services.geography.wpi_ingest")

    org_a = two_tenants["org_a"]
    await _seed_ports(session, org_a.id)
    original = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert original is not None
    original_lat = original.lat
    original_source = original.source_ref

    await wpi.ingest_wpi(
        session,
        organization_id=org_a.id,
        records=wpi.parse_wpi_records(sample_csv()),
        source_ref=WPI_SOURCE_REF,
    )
    await session.flush()
    session.expunge_all()

    await bind_tenant(session, org_a.id)
    gdynia = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert gdynia is not None
    assert gdynia.wpi_number == 28770
    assert gdynia.harbor_size == "Medium"
    assert gdynia.harbor_type == "Coastal Breakwater"
    assert gdynia.shelter == "Good"
    assert isinstance(gdynia.channel_depth_m, Decimal)
    assert gdynia.channel_depth_m == Decimal("11.0")
    assert gdynia.cargo_pier_depth_m == Decimal("9.4")
    assert gdynia.wpi_source_ref == WPI_SOURCE_REF
    assert gdynia.lat == original_lat
    assert gdynia.source_ref == original_source


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ingest_skips_rows_without_unlocode_and_unknown_ports(
    session,
    two_tenants,
) -> None:
    wpi = import_module("app.services.geography.wpi_ingest")

    org_a = two_tenants["org_a"]
    await _seed_ports(session, org_a.id)
    before = list((await session.scalars(select(Port))).all())

    await wpi.ingest_wpi(
        session,
        organization_id=org_a.id,
        records=wpi.parse_wpi_records(sample_csv()),
        source_ref=WPI_SOURCE_REF,
    )
    await session.flush()

    after = list((await session.scalars(select(Port))).all())
    assert {row.unlocode for row in after} == {row.unlocode for row in before}
    assert await session.scalar(select(Port).where(Port.unlocode == "ZZUNK")) is None
    skipped = await session.scalar(select(Port).where(Port.unlocode == "PLWAW"))
    assert skipped is not None
    assert skipped.wpi_number is None


def test_duplicate_wpi_rows_for_the_same_unlocode_are_a_domain_error() -> None:
    errors = import_module("app.domain.errors")
    parse_wpi_records = import_module("app.services.geography.wpi_ingest").parse_wpi_records

    doubled = sample_csv() + "28771,GDYNIA DUP,PL GDY,Small,Coastal Natural,Fair,8.0,7.0\n"
    with pytest.raises(errors.DuplicateWpiCode, match="PLGDY"):
        parse_wpi_records(doubled)


def test_wpi_ingest_never_opens_the_network() -> None:
    source = (_BACKEND / "app" / "services" / "geography" / "wpi_ingest.py").read_text(
        encoding="utf-8",
    )
    assert "httpx" not in source
    assert "urllib" not in source
    assert "requests" not in source


def test_terminals_endpoint_never_fetches_the_upstream_source() -> None:
    source = (_BACKEND / "app" / "api" / "terminals.py").read_text(encoding="utf-8")
    assert "httpx" not in source
    assert "urllib" not in source
    assert "github" not in source.lower()
    assert "nga.mil" not in source.lower()


def test_geography_agents_allows_terminal_and_keeps_ingest_offline() -> None:
    source = (_BACKEND / "app" / "services" / "geography" / "AGENTS.md").read_text(
        encoding="utf-8",
    )
    allowed, forbidden = source.split("## Zakaz", maxsplit=1)
    assert "app.models.terminal" in allowed
    assert "terminal" not in forbidden.lower()
    assert "World Port Index" not in forbidden
    assert "sieć w warstwie serwisu" in forbidden
