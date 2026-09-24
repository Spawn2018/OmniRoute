from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

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
        source_ref="fixture://charge-code/test",
        created_by=created_by,
    )


def _row(
    *,
    organization_id,
    created_by,
    template: str,
    token: str,
    start: date = date(2026, 1, 1),
    end: date = date(2026, 12, 31),
) -> ChargeTemplate:
    return ChargeTemplate(
        id=uuid4(),
        organization_id=organization_id,
        template_code=template,
        charge_code=token,
        valid_from=start,
        valid_until=end,
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_template_sequential_windows_allowed(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_code(organization_id=org_a.id, created_by=user_a.id, token="THC"))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            template="spot_thc",
            token="THC",
            start=date(2026, 1, 1),
            end=date(2026, 6, 30),
        )
    )
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            template="spot_thc",
            token="THC",
            start=date(2026, 7, 1),
            end=date(2026, 12, 31),
        )
    )
    await session.flush()
    rows = list((await session.scalars(select(ChargeTemplate))).all())
    assert len(rows) == 2


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_template_overlapping_window_is_refused(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_code(organization_id=org_a.id, created_by=user_a.id, token="THC"))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            template="spot_thc",
            token="THC",
        )
    )
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            template="spot_thc",
            token="THC",
            start=date(2026, 6, 1),
            end=date(2026, 8, 31),
        )
    )
    with pytest.raises(IntegrityError, match="ex_charge_template_no_overlap"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_template_same_span_other_tenant_is_allowed(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    await bind_tenant(session, org_a.id)
    session.add(_code(organization_id=org_a.id, created_by=user_a.id, token="THC"))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            template="spot_thc",
            token="THC",
        )
    )
    await session.flush()
    await bind_tenant(session, org_b.id)
    session.add(_code(organization_id=org_b.id, created_by=user_b.id, token="THC"))
    await session.flush()
    session.add(
        _row(
            organization_id=org_b.id,
            created_by=user_b.id,
            template="spot_thc",
            token="THC",
        )
    )
    await session.flush()
    visible = list((await session.scalars(select(ChargeTemplate))).all())
    assert len(visible) == 1
    assert visible[0].organization_id == org_b.id
