from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.port import Port
from app.models.port_surcharge import PortSurcharge

_UNLOCODE_SOURCE = "github:cristan/improved-un-locodes@fixture"
_MANUAL = "tenant:manual"


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


def _extra(*, organization_id: UUID, port_id: UUID, code: str, created_by: UUID) -> PortSurcharge:
    return PortSurcharge(
        id=uuid4(),
        organization_id=organization_id,
        amount=Decimal("85.0000"),
        currency="EUR",
        port_id=port_id,
        code=code,
        title=code.replace("_", " "),
        applies_when="kontener 40HC w weekend",
        source_ref=_MANUAL,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_port_surcharge_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    port_a = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port_a)
    await session.flush()
    extra_a = _extra(
        organization_id=org_a.id,
        port_id=port_a.id,
        code="thc",
        created_by=user_a.id,
    )
    session.add(extra_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    port_b = _port(organization_id=org_b.id, unlocode="DEHAM")
    session.add(port_b)
    await session.flush()
    extra_b = _extra(
        organization_id=org_b.id,
        port_id=port_b.id,
        code="thc",
        created_by=user_b.id,
    )
    session.add(extra_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PortSurcharge))).all())
    assert {row.id for row in visible_a} == {extra_a.id}
    assert await session.scalar(select(PortSurcharge).where(PortSurcharge.id == extra_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PortSurcharge))).all())
    assert {row.id for row in visible_b} == {extra_b.id}
    assert await session.scalar(select(PortSurcharge).where(PortSurcharge.id == extra_a.id)) is None
