from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import text

from app.core.database import bind_tenant
from app.models.charge import Charge
from tests.charges.test_charge_shipment_id import _shipment

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_489_creates_tree_margin_view() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "489_shipment_tree_margin.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "489_shipment_tree_margin"' in source
    assert 'down_revision: str | None = "488_charge_shipment_id"' in source
    assert "shipment_tree_margin" in source
    assert "security_invoker" in source
    assert "parent_shipment_id IS NULL" in source
    assert "create_table" not in source
    assert "httpx" not in source
    assert "DROP VIEW" in source.split("def downgrade")[1]


def test_tree_margin_select_does_not_sum_in_python() -> None:
    service = (
        _ROOT / "backend" / "app" / "services" / "charges" / "charge_service.py"
    ).read_text(encoding="utf-8")
    repository = (
        _ROOT / "backend" / "app" / "repositories" / "charges" / "charge_repository.py"
    ).read_text(encoding="utf-8")
    assert "list_tree_margins" in service
    assert "app.services.shipments" not in service
    assert "ShipmentTreeMargin" in repository
    assert "sum(" not in repository


def _charge(*, organization_id, user_id, shipment_id, buy: str, sell: str, currency: str) -> Charge:
    return Charge(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        buy_amount=Decimal(buy),
        buy_currency=currency,
        sell_amount=Decimal(sell),
        sell_currency=currency,
        shipment_id=shipment_id,
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tree_margin_rolls_root_and_direct_child(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]

    await bind_tenant(session, org_a.id)
    root = await _shipment(session, organization_id=org_a.id, user_id=user_a.id, suffix="root")
    child = await _shipment(
        session,
        organization_id=org_a.id,
        user_id=user_a.id,
        suffix="child",
        parent_shipment_id=root.id,
        relation_kind="drayage",
    )
    grandchild = await _shipment(
        session,
        organization_id=org_a.id,
        user_id=user_a.id,
        suffix="grand",
        parent_shipment_id=child.id,
        relation_kind="oncarriage",
    )
    session.add_all(
        [
            _charge(
                organization_id=org_a.id,
                user_id=user_a.id,
                shipment_id=root.id,
                buy="10.0000",
                sell="14.0000",
                currency="EUR",
            ),
            _charge(
                organization_id=org_a.id,
                user_id=user_a.id,
                shipment_id=child.id,
                buy="2.0000",
                sell="5.0000",
                currency="EUR",
            ),
            _charge(
                organization_id=org_a.id,
                user_id=user_a.id,
                shipment_id=grandchild.id,
                buy="7.0000",
                sell="9.0000",
                currency="EUR",
            ),
            _charge(
                organization_id=org_a.id,
                user_id=user_a.id,
                shipment_id=None,
                buy="100.0000",
                sell="100.0000",
                currency="EUR",
            ),
            _charge(
                organization_id=org_a.id,
                user_id=user_a.id,
                shipment_id=root.id,
                buy="1.0000",
                sell="3.0000",
                currency="USD",
            ),
        ],
    )
    await session.flush()

    rows = (
        await session.execute(
            text(
                "SELECT shipment_id, currency, buy_amount, sell_amount, "
                "margin_amount, charge_count FROM shipment_tree_margin "
                "ORDER BY currency"
            ),
        )
    ).all()
    by_currency = {row.currency: row for row in rows}
    assert set(by_currency) == {"EUR", "USD"}
    eur = by_currency["EUR"]
    assert eur.shipment_id == root.id
    assert eur.buy_amount == Decimal("12.0000")
    assert eur.sell_amount == Decimal("19.0000")
    assert eur.margin_amount == Decimal("7.0000")
    assert eur.charge_count == 2
    usd = by_currency["USD"]
    assert usd.shipment_id == root.id
    assert usd.margin_amount == Decimal("2.0000")
    assert child.id not in {row.shipment_id for row in rows}

    await bind_tenant(session, org_b.id)
    foreign = (
        await session.execute(text("SELECT shipment_id FROM shipment_tree_margin"))
    ).all()
    assert foreign == []
