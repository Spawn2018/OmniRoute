from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.charge_code import ChargeCode
from app.models.charge_template import ChargeTemplate


def _code(*, organization_id, created_by, token: str) -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=organization_id,
        code=token,
        name=token,
        aliases=[],
        created_by=created_by,
    )


def _row(*, organization_id, created_by, template: str, token: str) -> ChargeTemplate:
    return ChargeTemplate(
        id=uuid4(),
        organization_id=organization_id,
        template_code=template,
        charge_code=token,
        valid_from=date(2026, 1, 1),
        valid_until=date(2026, 12, 31),
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_template_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    session.add(_code(organization_id=org_a.id, created_by=user_a.id, token="THC"))
    await session.flush()
    row_a = _row(
        organization_id=org_a.id,
        created_by=user_a.id,
        template="spot_thc",
        token="THC",
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(_code(organization_id=org_b.id, created_by=user_b.id, token="THC"))
    await session.flush()
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        template="lane_thc",
        token="THC",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ChargeTemplate))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(ChargeTemplate).where(ChargeTemplate.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ChargeTemplate))).all())
    assert {row.id for row in visible_b} == {row_b.id}
