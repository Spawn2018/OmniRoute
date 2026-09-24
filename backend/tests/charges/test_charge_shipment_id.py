from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.domain.errors import InvalidShipment
from app.models.charge import Charge
from app.models.charge_code import ChargeCode
from app.models.party import Party
from app.models.quotation import Quotation
from app.models.rate_line import RateLine
from app.models.shipment import Shipment
from app.services.charges.charge_service import ChargeService

_ROOT = Path(__file__).resolve().parents[3]


def _catalog() -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code="THC",
        name="THC",
        aliases=[],
        source_ref="fixture://charge-code/test"
    )


def test_migration_488_adds_charge_shipment_fk() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "488_charge_shipment_id.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "488_charge_shipment_id"' in source
    assert 'down_revision: str | None = "487_container_destination_city"' in source
    assert "shipment_id" in source
    assert "fk_charge_shipment" in source
    assert '["organization_id", "shipment_id"]' in source
    assert "ondelete=\"RESTRICT\"" in source or "ondelete='RESTRICT'" in source
    assert "create_table" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "shipment_id" in source.split("def downgrade")[1]


def test_charge_service_does_not_import_shipments() -> None:
    source = (
        _ROOT / "backend" / "app" / "services" / "charges" / "charge_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.shipments" not in source
    assert "app.services.geography" not in source


@pytest.mark.asyncio
async def test_create_stores_optional_shipment_id() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    service = ChargeService(session)
    shipment_id = uuid4()

    created = await service.create_charge(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code="THC",
        buy_amount="10",
        buy_currency="EUR",
        sell_amount="14",
        sell_currency="EUR",
        rate_line_id=None,
        source_ref="tenant:manual",
        shipment_id=shipment_id,
    )

    assert created.shipment_id == shipment_id
    assert created.buy_amount is not None


@pytest.mark.asyncio
async def test_create_without_shipment_id_stays_null() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    service = ChargeService(session)

    created = await service.create_charge(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code="THC",
        buy_amount="10",
        buy_currency="EUR",
        sell_amount="14",
        sell_currency="EUR",
        rate_line_id=None,
        source_ref="tenant:manual",
    )

    assert created.shipment_id is None


@pytest.mark.asyncio
async def test_unknown_shipment_id_is_invalid_shipment() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    service = ChargeService(session)
    service._charges.add = AsyncMock(
        side_effect=IntegrityError("INSERT", {}, Exception("fk_charge_shipment")),
    )

    with pytest.raises(InvalidShipment, match="zlecenie"):
        await service.create_charge(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            buy_amount="10",
            buy_currency="EUR",
            sell_amount="14",
            sell_currency="EUR",
            rate_line_id=None,
            source_ref="tenant:manual",
            shipment_id=uuid4(),
        )


def _buy_rate(*, organization_id, created_by, source_ref: str) -> RateLine:
    return RateLine(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


def _party(*, organization_id, legal_name: str, created_by) -> Party:
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["customer"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=created_by,
    )


async def _shipment(
    session,
    *,
    organization_id,
    user_id,
    suffix: str,
    parent_shipment_id=None,
    relation_kind: str | None = None,
) -> Shipment:
    rate = _buy_rate(
        organization_id=organization_id,
        created_by=user_id,
        source_ref=f"tariff://charge-ship/{suffix}",
    )
    party = _party(
        organization_id=organization_id,
        legal_name=f"Klient {suffix}",
        created_by=user_id,
    )
    session.add_all([rate, party])
    await session.flush()
    quote = Quotation(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        rate_line_id=rate.id,
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=f"fixture://quote/{suffix}",
        created_by=user_id,
    )
    session.add(quote)
    await session.flush()
    ship = Shipment(
        id=uuid4(),
        organization_id=organization_id,
        quotation_id=quote.id,
        party_id=party.id,
        source_ref=f"fixture://shipment/{suffix}",
        status="draft",
        parent_shipment_id=parent_shipment_id,
        relation_kind=relation_kind,
        created_by=user_id,
    )
    session.add(ship)
    await session.flush()
    return ship


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_shipment_fk_stays_in_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _shipment(session, organization_id=org_a.id, user_id=user_a.id, suffix="a")
    linked = Charge(
        id=uuid4(),
        organization_id=org_a.id,
        charge_code="THC",
        buy_amount=Decimal("10.0000"),
        buy_currency="EUR",
        sell_amount=Decimal("14.0000"),
        sell_currency="EUR",
        shipment_id=ship_a.id,
        created_by=user_a.id,
    )
    blank = Charge(
        id=uuid4(),
        organization_id=org_a.id,
        charge_code="THC",
        buy_amount=Decimal("10.0000"),
        buy_currency="EUR",
        sell_amount=Decimal("12.0000"),
        sell_currency="EUR",
        created_by=user_a.id,
    )
    session.add_all([linked, blank])
    await session.flush()
    assert linked.shipment_id == ship_a.id
    assert blank.shipment_id is None

    await bind_tenant(session, org_b.id)
    ship_b = await _shipment(session, organization_id=org_b.id, user_id=user_b.id, suffix="b")

    await bind_tenant(session, org_a.id)
    foreign = Charge(
        id=uuid4(),
        organization_id=org_a.id,
        charge_code="THC",
        buy_amount=Decimal("10.0000"),
        buy_currency="EUR",
        sell_amount=Decimal("11.0000"),
        sell_currency="EUR",
        shipment_id=ship_b.id,
        created_by=user_a.id,
    )
    session.add(foreign)
    with pytest.raises(IntegrityError):
        await session.flush()
