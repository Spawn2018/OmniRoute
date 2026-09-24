from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    ChargeCodeConflict,
    InvalidChargeCode,
    InvalidSourceRef,
    UnknownChargeCode,
)
from app.models.charge_code import ChargeCode
from app.services.charge_codes.charge_code_service import ChargeCodeService


def _row(*, code: str, aliases: list[str] | None = None) -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=aliases or [],
        source_ref="fixture://charge-code/test",
    )


@pytest.mark.asyncio
async def test_create_normalizes_code_and_aliases() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = ChargeCodeService(session)

    created = await service.create_code(
        organization_id=uuid4(),
        user_id=uuid4(),
        code=" baf ",
        name=" Bunker Adjustment ",
        aliases=[" bunker ", "BAF_ADJ"],
        source_ref=" tenant:manual ",
    )

    assert created.code == "BAF"
    assert created.name == "Bunker Adjustment"
    assert created.aliases == ["BUNKER", "BAF_ADJ"]
    assert created.source_ref == "tenant:manual"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_blank_name() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = ChargeCodeService(session)
    with pytest.raises(InvalidChargeCode, match="nazwa"):
        await service.create_code(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="BAF",
            name="   ",
            aliases=[],
            source_ref="tenant:manual",
        )


@pytest.mark.asyncio
async def test_create_rejects_blank_source_ref() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = ChargeCodeService(session)
    with pytest.raises(InvalidSourceRef, match="source_ref"):
        await service.create_code(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="WAITING",
            name="Waiting",
            aliases=[],
            source_ref="   ",
        )


@pytest.mark.asyncio
async def test_create_rejects_alias_equal_to_code() -> None:
    service = ChargeCodeService(AsyncMock())
    with pytest.raises(InvalidChargeCode, match="alias"):
        await service.create_code(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="BAF",
            name="Bunker",
            aliases=["baf"],
            source_ref="tenant:manual",
        )


@pytest.mark.asyncio
async def test_create_rejects_token_already_in_catalog() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[None, _row(code="BAF")])
    service = ChargeCodeService(session)
    with pytest.raises(ChargeCodeConflict, match="BAF"):
        await service.create_code(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="XXX",
            name="Other",
            aliases=["baf"],
            source_ref="tenant:manual",
        )


@pytest.mark.asyncio
async def test_resolve_returns_catalog_row_for_alias() -> None:
    session = AsyncMock()
    row = _row(code="BAF", aliases=["BUNKER"])
    session.scalar = AsyncMock(return_value=row)
    service = ChargeCodeService(session)

    found = await service.resolve("bunker")
    assert found.code == "BAF"


@pytest.mark.asyncio
async def test_resolve_rejects_unknown_loose_string() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = ChargeCodeService(session)
    with pytest.raises(UnknownChargeCode, match="LOOSE"):
        await service.resolve("loose")


@pytest.mark.asyncio
async def test_list_codes_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _row(code="THC")
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = ChargeCodeService(session)

    listed = await service.list_codes()
    assert listed == [row]


@pytest.mark.asyncio
async def test_seed_omni_exp1_inserts_missing_only() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = ChargeCodeService(session)

    created = await service.seed_omni_exp1(
        organization_id=uuid4(),
        user_id=uuid4(),
    )
    assert {row.code for row in created} == {"WAITING", "NO_SHOW", "DIVERSION", "STAMP"}
    assert all(row.source_ref == "omni:charge-code:exp1" for row in created)

    session.scalar = AsyncMock(return_value=created[0])
    again = await service.seed_omni_exp1(
        organization_id=uuid4(),
        user_id=uuid4(),
    )
    assert again == []
