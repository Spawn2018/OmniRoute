from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import CommodityCodeConflict, InvalidCommodityCode, UnknownCommodityCode
from app.models.commodity_code import CommodityCode
from app.services.commodity_codes.commodity_code_service import CommodityCodeService


def _row(*, code: str, aliases: list[str] | None = None) -> CommodityCode:
    return CommodityCode(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=aliases or [],
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_normalizes_code_and_aliases() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = CommodityCodeService(session)

    created = await service.create_code(
        organization_id=uuid4(),
        user_id=uuid4(),
        code=" 0805 ",
        name=" Citrus ",
        aliases=[" 080510 "],
    )

    assert created.code == "0805"
    assert created.name == "Citrus"
    assert created.aliases == ["080510"]
    assert created.source_ref == "tenant:manual"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_blank_name() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = CommodityCodeService(session)
    with pytest.raises(InvalidCommodityCode, match="nazwa"):
        await service.create_code(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="0805",
            name="   ",
            aliases=[],
        )


@pytest.mark.asyncio
async def test_create_rejects_alias_equal_to_code() -> None:
    service = CommodityCodeService(AsyncMock())
    with pytest.raises(InvalidCommodityCode, match="alias"):
        await service.create_code(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="0805",
            name="Citrus",
            aliases=["0805"],
        )


@pytest.mark.asyncio
async def test_create_rejects_token_already_in_catalog() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[None, _row(code="0805")])
    service = CommodityCodeService(session)
    with pytest.raises(CommodityCodeConflict, match="0805"):
        await service.create_code(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="0901",
            name="Coffee",
            aliases=["0805"],
        )


@pytest.mark.asyncio
async def test_resolve_returns_catalog_row_for_alias() -> None:
    session = AsyncMock()
    row = _row(code="0805", aliases=["080510"])
    session.scalar = AsyncMock(return_value=row)
    service = CommodityCodeService(session)

    found = await service.resolve("080510")
    assert found.code == "0805"


@pytest.mark.asyncio
async def test_resolve_rejects_unknown_loose_string() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = CommodityCodeService(session)
    with pytest.raises(UnknownCommodityCode, match="9999"):
        await service.resolve("9999")


@pytest.mark.asyncio
async def test_list_codes_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _row(code="0805")
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = CommodityCodeService(session)

    listed = await service.list_codes()
    assert listed == [row]
