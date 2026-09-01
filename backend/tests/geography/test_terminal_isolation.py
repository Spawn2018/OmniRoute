from importlib import import_module
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.port import Port

_MANUAL = "tenant:manual"
_UNLOCODE_SOURCE = "github:cristan/improved-un-locodes@fixture"


def _port(*, organization_id: UUID, unlocode: str) -> Port:
    return Port(
        id=uuid4(),
        organization_id=organization_id,
        unlocode=unlocode,
        name=unlocode,
        country_code=unlocode[:2],
        is_seaport=True,
        function_flags=["port"],
        aliases=[],
        is_official=True,
        source_ref=_UNLOCODE_SOURCE,
    )


def _terminal_cls():
    return import_module("app.models.terminal").Terminal


def _terminal(
    *,
    organization_id: UUID,
    port_id: UUID,
    name: str,
    isps_code: str | None = None,
    created_by: UUID | None = None,
):
    return _terminal_cls()(
        id=uuid4(),
        organization_id=organization_id,
        port_id=port_id,
        name=name,
        isps_code=isps_code,
        operator_name=None,
        source_ref=_MANUAL,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    Terminal = _terminal_cls()

    await bind_tenant(session, org_a.id)
    port_a = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port_a)
    await session.flush()
    terminal_a = _terminal(
        organization_id=org_a.id,
        port_id=port_a.id,
        name="BCT Gdynia",
        isps_code="PLGDY-BCT",
        created_by=two_tenants["user_a"].id,
    )
    session.add(terminal_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    port_b = _port(organization_id=org_b.id, unlocode="DEHAM")
    session.add(port_b)
    await session.flush()
    terminal_b = _terminal(
        organization_id=org_b.id,
        port_id=port_b.id,
        name="HHLA",
        isps_code="DEHAM-HHLA",
        created_by=two_tenants["user_b"].id,
    )
    session.add(terminal_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Terminal))).all())
    assert {row.id for row in visible_a} == {terminal_a.id}
    assert await session.scalar(select(Terminal).where(Terminal.id == terminal_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Terminal))).all())
    assert {row.id for row in visible_b} == {terminal_b.id}
    assert await session.scalar(select(Terminal).where(Terminal.id == terminal_a.id)) is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_may_not_point_at_another_tenant_port(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    await bind_tenant(session, org_a.id)
    port_a = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(
        _terminal(
            organization_id=org_b.id,
            port_id=port_a.id,
            name="BCT obcy port",
        )
    )
    with pytest.raises(IntegrityError, match="fk_terminal_port"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_isps_code_is_unique_inside_one_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    port = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port)
    await session.flush()
    session.add(
        _terminal(
            organization_id=org_a.id,
            port_id=port.id,
            name="BCT",
            isps_code="PLGDY-BCT",
        )
    )
    await session.flush()
    session.add(
        _terminal(
            organization_id=org_a.id,
            port_id=port.id,
            name="Inny nabrzeże",
            isps_code="PLGDY-BCT",
        )
    )
    with pytest.raises(IntegrityError, match="uq_terminal_org_isps"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_two_tenants_may_hold_the_same_isps_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    await bind_tenant(session, org_a.id)
    port_a = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port_a)
    await session.flush()
    session.add(
        _terminal(
            organization_id=org_a.id,
            port_id=port_a.id,
            name="BCT",
            isps_code="PLGDY-BCT",
        )
    )
    await session.flush()

    await bind_tenant(session, org_b.id)
    port_b = _port(organization_id=org_b.id, unlocode="PLGDY")
    session.add(port_b)
    await session.flush()
    session.add(
        _terminal(
            organization_id=org_b.id,
            port_id=port_b.id,
            name="BCT",
            isps_code="PLGDY-BCT",
        )
    )
    await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_two_unnamed_isps_terminals_at_the_same_port_cannot_share_a_name(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    port = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port)
    await session.flush()
    session.add(_terminal(organization_id=org_a.id, port_id=port.id, name="Nabrzeże 1"))
    await session.flush()
    session.add(_terminal(organization_id=org_a.id, port_id=port.id, name="Nabrzeże 1"))
    with pytest.raises(IntegrityError, match="uq_terminal_org_port_name"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_without_tenant_context_is_invisible(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    Terminal = _terminal_cls()

    await bind_tenant(session, org_a.id)
    port = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port)
    await session.flush()
    session.add(_terminal(organization_id=org_a.id, port_id=port.id, name="BCT"))
    await session.flush()
    session.expunge_all()

    await session.execute(text("SELECT set_config('app.current_org', '', true)"))
    assert list((await session.scalars(select(Terminal))).all()) == []


def test_terminal_organization_id_rejects_null() -> None:
    column = _terminal_cls().__table__.c.organization_id
    assert column.nullable is False
