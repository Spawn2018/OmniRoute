from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    ChargeRateMismatch,
    InvalidMoney,
    MixedCurrencyCharge,
    ResourceNotFound,
    UnknownChargeCode,
)
from app.models.charge import Charge
from app.models.charge_code import ChargeCode
from app.models.rate_line import RateLine
from app.services.charges.charge_service import ChargeService
from app.services.extraction import extraction_service as extraction_module


def _catalog(*, code: str = "THC") -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=[],
    )


def _rate(*, charge_code: str = "THC") -> RateLine:
    return RateLine(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code=charge_code,
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
    )


def _charge() -> Charge:
    return Charge(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code="THC",
        buy_amount=Decimal("10.0000"),
        buy_currency="EUR",
        sell_amount=Decimal("14.0000"),
        sell_currency="EUR",
    )


@pytest.mark.asyncio
async def test_get_charge_returns_row() -> None:
    service = ChargeService(AsyncMock())
    row = _charge()
    service._charges.get = AsyncMock(return_value=row)
    assert await service.get_charge(row.id) is row


@pytest.mark.asyncio
async def test_get_charge_unknown_is_not_found() -> None:
    service = ChargeService(AsyncMock())
    service._charges.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound, match="nieznana opłata"):
        await service.get_charge(uuid4())


@pytest.mark.asyncio
async def test_create_stores_buy_sell_on_one_row() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog(code="THC"))
    service = ChargeService(session)

    created = await service.create_charge(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code=" thc ",
        buy_amount="10.5",
        buy_currency="EUR",
        sell_amount="14",
        sell_currency="EUR",
        rate_line_id=None,
    )

    assert created.charge_code == "THC"
    assert created.buy_amount == Decimal("10.5000")
    assert created.sell_amount == Decimal("14.0000")
    assert created.buy_currency == "EUR"
    assert created.sell_currency == "EUR"
    assert created.rate_line_id is None
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_float_buy() -> None:
    service = ChargeService(AsyncMock())
    with pytest.raises(InvalidMoney, match="float"):
        await service.create_charge(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            buy_amount=10.5,
            buy_currency="EUR",
            sell_amount="14",
            sell_currency="EUR",
            rate_line_id=None,
        )


@pytest.mark.asyncio
async def test_create_rejects_mixed_currency() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    service = ChargeService(session)
    with pytest.raises(MixedCurrencyCharge, match="tę samą walutę"):
        await service.create_charge(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            buy_amount="10",
            buy_currency="EUR",
            sell_amount="14",
            sell_currency="USD",
            rate_line_id=None,
        )


@pytest.mark.asyncio
async def test_create_rejects_unknown_charge_code() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = ChargeService(session)
    with pytest.raises(UnknownChargeCode, match="LOOSE"):
        await service.create_charge(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="loose",
            buy_amount="10",
            buy_currency="EUR",
            sell_amount="14",
            sell_currency="EUR",
            rate_line_id=None,
        )


@pytest.mark.asyncio
async def test_create_links_existing_rate_line() -> None:
    session = AsyncMock()
    rate = _rate(charge_code="THC")
    session.scalar = AsyncMock(return_value=_catalog(code="THC"))
    session.get = AsyncMock(return_value=rate)
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = ChargeService(session)

    created = await service.create_charge(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code="THC",
        buy_amount="10",
        buy_currency="EUR",
        sell_amount="14",
        sell_currency="EUR",
        rate_line_id=rate.id,
    )

    assert created.rate_line_id == rate.id


@pytest.mark.asyncio
async def test_create_rejects_missing_rate_line() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    session.get = AsyncMock(return_value=None)
    service = ChargeService(session)
    with pytest.raises(ResourceNotFound, match="rate_line"):
        await service.create_charge(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            buy_amount="10",
            buy_currency="EUR",
            sell_amount="14",
            sell_currency="EUR",
            rate_line_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_create_rejects_rate_line_with_other_charge_code() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog(code="THC"))
    session.get = AsyncMock(return_value=_rate(charge_code="BAF"))
    service = ChargeService(session)
    with pytest.raises(ChargeRateMismatch, match="stawką kupna"):
        await service.create_charge(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            buy_amount="10",
            buy_currency="EUR",
            sell_amount="14",
            sell_currency="EUR",
            rate_line_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_list_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _charge()
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = ChargeService(session)

    listed = await service.list_charges()
    assert listed == [row]


def test_extraction_service_does_not_import_rates_or_charges() -> None:
    source = Path(extraction_module.__file__).read_text(encoding="utf-8")
    assert "from app.services.rate_lines" not in source
    assert "from app.repositories.rate_lines" not in source
    assert "from app.services.charges" not in source
    assert "from app.repositories.charges" not in source
    assert "from app.services.quotations" not in source
    assert "from app.repositories.quotations" not in source
    assert "from app.services.organization_settings" not in source
