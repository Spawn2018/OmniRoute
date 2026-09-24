from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    InvalidMoney,
    InvalidRateLine,
    InvalidSourceRef,
    RateLineAlreadySuperseded,
    ResourceNotFound,
    UnknownChargeCode,
)
from app.models.charge_code import ChargeCode
from app.models.fuel_index import FuelIndex
from app.models.rate_line import RateLine
from app.services.rate_lines.rate_line_service import RateLineService


def _catalog(*, code: str = "THC") -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=[],
        source_ref="fixture://charge-code/test"
    )


def _fuel_index() -> FuelIndex:
    return FuelIndex(
        id=uuid4(),
        organization_id=uuid4(),
        index_kind="fsc",
        published_on=date(2026, 9, 1),
        index_value=Decimal("1.1000"),
        source_ref="fixture://fuel-index/test",
    )


def _rate(*, charge_code: str = "THC", superseded_by=None) -> RateLine:
    return RateLine(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code=charge_code,
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
        superseded_by=superseded_by,
    )


@pytest.mark.asyncio
async def test_create_stores_money_and_resolved_catalog_code() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog(code="THC"))
    service = RateLineService(session)

    created = await service.create_buy_rate(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code=" thc ",
        amount="12.5",
        currency="EUR",
        source_ref=" tariff://msc-2026 ",
    )

    assert created.charge_code == "THC"
    assert created.amount == Decimal("12.5000")
    assert created.currency == "EUR"
    assert created.source_ref == "tariff://msc-2026"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_blank_source_ref() -> None:
    service = RateLineService(AsyncMock())
    with pytest.raises(InvalidSourceRef, match="obowiązkowy"):
        await service.create_buy_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            amount="10",
            currency="EUR",
            source_ref="  ",
        )


@pytest.mark.asyncio
async def test_create_rejects_float_amount() -> None:
    service = RateLineService(AsyncMock())
    with pytest.raises(InvalidMoney, match="float"):
        await service.create_buy_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            amount=10.5,
            currency="EUR",
            source_ref="tariff://a",
        )


@pytest.mark.asyncio
async def test_create_rejects_unknown_charge_code() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = RateLineService(session)
    with pytest.raises(UnknownChargeCode, match="LOOSE"):
        await service.create_buy_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="loose",
            amount="10",
            currency="EUR",
            source_ref="tariff://a",
        )


@pytest.mark.asyncio
async def test_create_with_fuel_index_id() -> None:
    session = AsyncMock()
    index = _fuel_index()
    session.get = AsyncMock(return_value=index)
    session.scalar = AsyncMock(return_value=_catalog(code="THC"))
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = RateLineService(session)

    created = await service.create_buy_rate(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code="THC",
        amount="10",
        currency="EUR",
        source_ref="tariff://fsc-fk",
        fuel_index_id=index.id,
    )

    assert created.fuel_index_id == index.id
    session.get.assert_awaited()


@pytest.mark.asyncio
async def test_create_rejects_unknown_fuel_index_id() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    service = RateLineService(session)
    with pytest.raises(InvalidRateLine, match="fuel_index"):
        await service.create_buy_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            amount="10",
            currency="EUR",
            source_ref="tariff://fsc-fk",
            fuel_index_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_supersede_writes_new_row_and_points_predecessor() -> None:
    session = AsyncMock()
    current = _rate()
    session.get = AsyncMock(return_value=current)
    session.scalar = AsyncMock(return_value=_catalog(code="THC"))
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = RateLineService(session)

    successor = await service.supersede(
        rate_line_id=current.id,
        user_id=uuid4(),
        amount="11",
        currency="EUR",
        source_ref="tariff://b",
    )

    assert successor.amount == Decimal("11.0000")
    assert successor.source_ref == "tariff://b"
    assert current.superseded_by == successor.id
    assert successor.id != current.id


@pytest.mark.asyncio
async def test_supersede_rejects_missing_row() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    service = RateLineService(session)
    with pytest.raises(ResourceNotFound, match="rate_line"):
        await service.supersede(
            rate_line_id=uuid4(),
            user_id=uuid4(),
            amount="11",
            currency="EUR",
            source_ref="tariff://b",
        )


@pytest.mark.asyncio
async def test_supersede_rejects_already_superseded() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=_rate(superseded_by=uuid4()))
    service = RateLineService(session)
    with pytest.raises(RateLineAlreadySuperseded, match="zastąpiony"):
        await service.supersede(
            rate_line_id=uuid4(),
            user_id=uuid4(),
            amount="11",
            currency="EUR",
            source_ref="tariff://b",
        )


@pytest.mark.asyncio
async def test_list_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _rate()
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = RateLineService(session)

    listed = await service.list_rates()
    assert listed == [row]
