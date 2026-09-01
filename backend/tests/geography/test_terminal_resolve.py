from decimal import Decimal
from importlib import import_module

import pytest
from hypothesis import given
from hypothesis import strategies as st
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.port import Port
from app.services.geography.unlocode_ingest import ingest_ports
from tests.geography.unlocode_fixture import FIXTURE_SOURCE_REF, sample_records


async def _seed_ports(session, organization_id) -> None:
    await bind_tenant(session, organization_id)
    await ingest_ports(
        session,
        organization_id=organization_id,
        records=sample_records(),
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_maps_isps_code_to_the_terminal(session, two_tenants) -> None:
    TerminalService = import_module("app.services.geography.terminal_service").TerminalService

    org_a = two_tenants["org_a"]
    await _seed_ports(session, org_a.id)
    port = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert port is not None

    service = TerminalService(session)
    created = await service.create_terminal(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        port_id=port.id,
        name="BCT Gdynia",
        isps_code="plgdy-bct",
        operator_name="BCT",
        lat=None,
        lng=None,
    )

    resolved = await service.resolve("PLGDY-BCT")
    assert resolved.id == created.id
    assert resolved.isps_code == "PLGDY-BCT"
    assert resolved.source_ref == "tenant:manual"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_ignores_letter_case_of_the_isps_code(session, two_tenants) -> None:
    TerminalService = import_module("app.services.geography.terminal_service").TerminalService

    org_a = two_tenants["org_a"]
    await _seed_ports(session, org_a.id)
    port = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert port is not None

    service = TerminalService(session)
    await service.create_terminal(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        port_id=port.id,
        name="BCT Gdynia",
        isps_code="PLGDY-BCT",
        operator_name=None,
        lat=None,
        lng=None,
    )

    assert (await service.resolve("plgdy-bct")).isps_code == "PLGDY-BCT"
    assert (await service.resolve(" PlGdy-Bct ")).isps_code == "PLGDY-BCT"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_rejects_an_isps_code_outside_the_catalog(session, two_tenants) -> None:
    errors = import_module("app.domain.errors")
    TerminalService = import_module("app.services.geography.terminal_service").TerminalService

    org_a = two_tenants["org_a"]
    await _seed_ports(session, org_a.id)

    with pytest.raises(errors.UnknownTerminal, match="GHOST"):
        await TerminalService(session).resolve("GHOST-1")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_never_reaches_into_another_tenant_catalog(session, two_tenants) -> None:
    errors = import_module("app.domain.errors")
    TerminalService = import_module("app.services.geography.terminal_service").TerminalService

    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    await _seed_ports(session, org_a.id)
    port = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    assert port is not None
    await TerminalService(session).create_terminal(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        port_id=port.id,
        name="BCT Gdynia",
        isps_code="PLGDY-BCT",
        operator_name=None,
        lat=None,
        lng=None,
    )

    await bind_tenant(session, org_b.id)
    with pytest.raises(errors.UnknownTerminal, match="PLGDY-BCT"):
        await TerminalService(session).resolve("PLGDY-BCT")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_terminals_narrows_to_the_chosen_port(session, two_tenants) -> None:
    TerminalService = import_module("app.services.geography.terminal_service").TerminalService

    org_a = two_tenants["org_a"]
    await _seed_ports(session, org_a.id)
    gdynia = await session.scalar(select(Port).where(Port.unlocode == "PLGDY"))
    hamburg = await session.scalar(select(Port).where(Port.unlocode == "DEHAM"))
    assert gdynia is not None
    assert hamburg is not None

    service = TerminalService(session)
    await service.create_terminal(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        port_id=gdynia.id,
        name="BCT Gdynia",
        isps_code="PLGDY-BCT",
        operator_name=None,
        lat=Decimal("54.53"),
        lng=Decimal("18.55"),
    )
    await service.create_terminal(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        port_id=hamburg.id,
        name="HHLA",
        isps_code="DEHAM-HHLA",
        operator_name=None,
        lat=None,
        lng=None,
    )

    found = await service.list_terminals(port_id=gdynia.id)
    assert {row.name for row in found} == {"BCT Gdynia"}


_ISPS = st.from_regex(r"[A-Z0-9]{4,16}", fullmatch=True)


@given(code=_ISPS)
def test_normalize_isps_code_is_idempotent_and_case_insensitive(code: str) -> None:
    normalize_isps_code = import_module("app.domain.terminal").normalize_isps_code

    assert normalize_isps_code(code) == code
    assert normalize_isps_code(code.lower()) == code


def test_normalize_isps_code_treats_blank_as_absent() -> None:
    normalize_isps_code = import_module("app.domain.terminal").normalize_isps_code

    assert normalize_isps_code("   ") is None
    assert normalize_isps_code(None) is None


def test_unknown_terminal_is_a_domain_error() -> None:
    errors = import_module("app.domain.errors")
    assert issubclass(errors.UnknownTerminal, errors.DomainError)


def test_duplicate_wpi_code_is_a_domain_error() -> None:
    errors = import_module("app.domain.errors")
    assert issubclass(errors.DuplicateWpiCode, errors.DomainError)
