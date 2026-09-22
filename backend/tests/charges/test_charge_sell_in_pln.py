from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import text

from app.core.database import bind_tenant
from app.domain.errors import InvalidNbpRate, ResourceNotFound
from app.models.charge import Charge
from app.models.nbp_rate import NbpRate
from app.services.charges.charge_service import ChargeService

_ROOT = Path(__file__).resolve().parents[3]


def _charge(
    *,
    organization_id,
    created_by,
    sell: str,
    currency: str,
) -> Charge:
    return Charge(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        buy_amount=Decimal("10.0000"),
        buy_currency=currency,
        sell_amount=Decimal(sell),
        sell_currency=currency,
        source_ref="fixture://charge/sell-in-pln",
        created_by=created_by,
    )


def _rate(
    *,
    organization_id,
    created_by,
    currency: str,
    rate_date: date,
    mid: str,
) -> NbpRate:
    return NbpRate(
        id=uuid4(),
        organization_id=organization_id,
        currency=currency,
        rate_date=rate_date,
        mid=Decimal(mid),
        source_ref=f"fixture://nbp/{currency}/{rate_date.isoformat()}",
        created_by=created_by,
    )


def test_migration_492_defines_charge_sell_in_pln() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "492_charge_sell_in_pln.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "492_charge_sell_in_pln"' in source
    assert 'down_revision: str | None = "491_task"' in source
    assert "CREATE FUNCTION charge_sell_in_pln" in source
    assert "sell_amount * r.mid" in source
    assert "create_table" not in source
    assert "httpx" not in source


def test_charge_service_does_not_import_nbp_rates_or_multiply() -> None:
    service = (
        _ROOT / "backend" / "app" / "services" / "charges" / "charge_service.py"
    ).read_text(encoding="utf-8")
    repository = (
        _ROOT
        / "backend"
        / "app"
        / "repositories"
        / "charges"
        / "charge_repository.py"
    ).read_text(encoding="utf-8")
    assert "app.services.nbp_rates" not in service
    assert "app.services.nbp_rates" not in repository
    assert " * " not in service
    assert "charge_sell_in_pln" in repository
    assert "float(" not in service
    assert "float(" not in repository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sell_in_pln_returns_sell_for_pln(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    day = date(2026, 9, 1)
    row = _charge(
        organization_id=org_a.id,
        created_by=user_a.id,
        sell="14.0000",
        currency="PLN",
    )
    await bind_tenant(session, org_a.id)
    session.add(row)
    await session.flush()
    amount = await ChargeService(session).sell_in_pln(charge_id=row.id, on_date=day)
    assert amount == Decimal("14.0000")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sell_in_pln_multiplies_foreign_currency(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    day = date(2026, 9, 1)
    row = _charge(
        organization_id=org_a.id,
        created_by=user_a.id,
        sell="14.0000",
        currency="EUR",
    )
    rate = _rate(
        organization_id=org_a.id,
        created_by=user_a.id,
        currency="EUR",
        rate_date=day,
        mid="4.2500",
    )
    await bind_tenant(session, org_a.id)
    session.add_all([row, rate])
    await session.flush()
    amount = await ChargeService(session).sell_in_pln(charge_id=row.id, on_date=day)
    assert amount == Decimal("59.5000")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sell_in_pln_missing_rate_is_kurs(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    day = date(2026, 9, 1)
    row = _charge(
        organization_id=org_a.id,
        created_by=user_a.id,
        sell="14.0000",
        currency="EUR",
    )
    await bind_tenant(session, org_a.id)
    session.add(row)
    await session.flush()
    with pytest.raises(InvalidNbpRate, match="kurs"):
        await ChargeService(session).sell_in_pln(charge_id=row.id, on_date=day)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sell_in_pln_ignores_foreign_tenant_rate(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    day = date(2026, 9, 1)
    row = _charge(
        organization_id=org_a.id,
        created_by=user_a.id,
        sell="14.0000",
        currency="EUR",
    )
    foreign_rate = _rate(
        organization_id=org_b.id,
        created_by=user_b.id,
        currency="EUR",
        rate_date=day,
        mid="9.9900",
    )
    await bind_tenant(session, org_b.id)
    session.add(foreign_rate)
    await session.flush()
    await bind_tenant(session, org_a.id)
    session.add(row)
    await session.flush()
    with pytest.raises(InvalidNbpRate, match="kurs"):
        await ChargeService(session).sell_in_pln(charge_id=row.id, on_date=day)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sell_in_pln_unknown_charge(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    with pytest.raises(ResourceNotFound, match="opłat"):
        await ChargeService(session).sell_in_pln(
            charge_id=uuid4(),
            on_date=date(2026, 9, 1),
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sell_in_pln_function_exists(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    exists = await session.scalar(
        text(
            "SELECT 1 FROM pg_proc WHERE proname = 'charge_sell_in_pln'",
        ),
    )
    assert exists == 1
