from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import QuotationGap, UnknownChargeCode
from app.models.charge_code import ChargeCode
from app.models.quotation import Quotation
from app.repositories.quotations.quotation_repository import QUOTE_FROM_CURRENT_SQL
from app.services.extraction import extraction_service as extraction_module
from app.services.quotations.quotation_service import QuotationService


def _catalog(*, code: str = "THC") -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=[],
        source_ref="fixture://charge-code/test"
    )


def _quoted(*, code: str = "THC") -> Quotation:
    from decimal import Decimal

    return Quotation(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code=code,
        rate_line_id=uuid4(),
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
    )


def _row_mapping(row: Quotation) -> dict[str, object]:
    return {
        "id": row.id,
        "organization_id": row.organization_id,
        "charge_code": row.charge_code,
        "rate_line_id": row.rate_line_id,
        "amount": row.amount,
        "currency": row.currency,
        "source_ref": row.source_ref,
        "created_by": None,
        "origin_port_id": None,
        "destination_port_id": None,
        "party_id": None,
    }


def _execute_returning(mapping: dict[str, object] | None) -> MagicMock:
    mappings = MagicMock()
    mappings.first.return_value = mapping
    execute_result = MagicMock()
    execute_result.mappings.return_value = mappings
    return execute_result


def test_quote_sql_selects_current_rate_line_amount() -> None:
    sql = " ".join(QUOTE_FROM_CURRENT_SQL.split())
    assert "INSERT INTO quotation" in sql
    assert "SELECT" in sql
    assert "FROM rate_line" in sql
    assert "superseded_by IS NULL" in sql
    assert "rl.amount" in sql
    assert "LIMIT 1" in sql


@pytest.mark.asyncio
async def test_quote_copies_amount_from_sql_not_request() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    mappings = MagicMock()
    row = _quoted()
    mappings.first.return_value = {
        "id": row.id,
        "organization_id": row.organization_id,
        "charge_code": row.charge_code,
        "rate_line_id": row.rate_line_id,
        "amount": row.amount,
        "currency": row.currency,
        "source_ref": row.source_ref,
        "created_by": None,
        "origin_port_id": None,
        "destination_port_id": None,
        "party_id": None,
    }
    execute_result = MagicMock()
    execute_result.mappings.return_value = mappings
    session.execute = AsyncMock(return_value=execute_result)
    service = QuotationService(session)

    quoted = await service.quote_from_current_rate(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code=" thc ",
        origin_port_id=uuid4(),
        destination_port_id=uuid4(),
        party_id=uuid4(),
    )

    assert quoted.amount == row.amount
    assert quoted.currency == "EUR"
    assert quoted.charge_code == "THC"
    session.execute.assert_awaited()


@pytest.mark.asyncio
async def test_quote_gap_when_no_current_rate() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    mappings = MagicMock()
    mappings.first.return_value = None
    execute_result = MagicMock()
    execute_result.mappings.return_value = mappings
    session.execute = AsyncMock(return_value=execute_result)
    service = QuotationService(session)

    with pytest.raises(QuotationGap, match="THC"):
        await service.quote_from_current_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_quote_rejects_unknown_charge_code() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = QuotationService(session)
    with pytest.raises(UnknownChargeCode, match="LOOSE"):
        await service.quote_from_current_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="loose",
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_list_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _quoted()
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = QuotationService(session)

    listed = await service.list_quotations()
    assert listed == [row]


@pytest.mark.asyncio
async def test_quote_batch_runs_sql_per_code() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[_catalog(code="THC"), _catalog(code="BAF")])
    thc = _quoted(code="THC")
    baf = _quoted(code="BAF")
    session.execute = AsyncMock(
        side_effect=[
            _execute_returning(_row_mapping(thc)),
            _execute_returning(_row_mapping(baf)),
        ]
    )
    service = QuotationService(session)
    origin = uuid4()
    destination = uuid4()
    party = uuid4()

    quoted = await service.quote_batch_from_current_rates(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_codes=["thc", "BAF"],
        origin_port_id=origin,
        destination_port_id=destination,
        party_id=party,
    )

    assert [row.charge_code for row in quoted] == ["THC", "BAF"]
    assert session.execute.await_count == 2


@pytest.mark.asyncio
async def test_quote_batch_gap_on_second_code_stops() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[_catalog(code="THC"), _catalog(code="BAF")])
    thc = _quoted(code="THC")
    session.execute = AsyncMock(
        side_effect=[
            _execute_returning(_row_mapping(thc)),
            _execute_returning(None),
        ]
    )
    service = QuotationService(session)

    with pytest.raises(QuotationGap, match="BAF"):
        await service.quote_batch_from_current_rates(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_codes=["THC", "BAF"],
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )
    assert session.execute.await_count == 2


@pytest.mark.asyncio
async def test_set_negotiated_channel_quote_stores_id() -> None:
    session = AsyncMock()
    row = _quoted()
    service = QuotationService(session)
    service._quotations.get = AsyncMock(return_value=row)
    service._quotations.save = AsyncMock(side_effect=lambda saved: saved)
    channel_id = uuid4()
    saved = await service.set_negotiated_channel_quote(row.id, channel_id)
    assert saved.negotiated_channel_quote_id == channel_id
    assert saved.amount == row.amount


def test_extraction_service_does_not_import_quotations() -> None:
    source = Path(extraction_module.__file__).read_text(encoding="utf-8")
    assert "from app.services.quotations" not in source
    assert "from app.repositories.quotations" not in source
    assert "from app.models.quotation" not in source
    assert "from app.services.rate_lines" not in source
    assert "from app.repositories.rate_lines" not in source
