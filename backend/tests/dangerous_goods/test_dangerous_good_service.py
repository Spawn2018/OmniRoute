from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    DangerousGoodConflict,
    InvalidDangerousGood,
    InvalidImdgClass,
    UnknownDangerousGood,
)
from app.models.dangerous_good import DangerousGood
from app.services.dangerous_goods.dangerous_good_service import DangerousGoodService


def _row(*, un_number: str, aliases: list[str] | None = None) -> DangerousGood:
    return DangerousGood(
        id=uuid4(),
        organization_id=uuid4(),
        un_number=un_number,
        imdg_class="3",
        adr_tunnel_code="D",
        segregation_group="none",
            packing_group="II",
        marine_pollutant=False,
            limited_quantity=False,
        name=un_number,
        aliases=aliases or [],
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_normalizes_un_number_and_class() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = DangerousGoodService(session)

    created = await service.create_good(
        organization_id=uuid4(),
        user_id=uuid4(),
        un_number=" UN1203 ",
        imdg_class="3",
        name=" Petrol ",
        aliases=[" 1213 "],
        adr_tunnel_code="D",
        segregation_group="sg1",
            packing_group="II",
        marine_pollutant=False,
            limited_quantity=False,
    )

    assert created.un_number == "1203"
    assert created.imdg_class == "3"
    assert created.adr_tunnel_code == "D"
    assert created.segregation_group == "sg1"
    assert created.packing_group == "II"
    assert created.marine_pollutant is False
    assert created.limited_quantity is False
    assert created.name == "Petrol"
    assert created.aliases == ["1213"]
    assert created.source_ref == "tenant:manual"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_blank_name() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = DangerousGoodService(session)
    with pytest.raises(InvalidDangerousGood, match="nazwa"):
        await service.create_good(
            organization_id=uuid4(),
            user_id=uuid4(),
            un_number="1203",
            imdg_class="3",
            name="   ",
            aliases=[],
            adr_tunnel_code="D",
            segregation_group="none",
            packing_group="II",
            marine_pollutant=False,
            limited_quantity=False,
        )


@pytest.mark.asyncio
async def test_create_rejects_unknown_imdg_class() -> None:
    service = DangerousGoodService(AsyncMock())
    with pytest.raises(InvalidImdgClass, match="allowlisty"):
        await service.create_good(
            organization_id=uuid4(),
            user_id=uuid4(),
            un_number="1203",
            imdg_class="3.9",
            name="Petrol",
            aliases=[],
            adr_tunnel_code="D",
            segregation_group="none",
            packing_group="II",
            marine_pollutant=False,
            limited_quantity=False,
        )


@pytest.mark.asyncio
async def test_create_rejects_alias_equal_to_un_number() -> None:
    service = DangerousGoodService(AsyncMock())
    with pytest.raises(InvalidDangerousGood, match="alias"):
        await service.create_good(
            organization_id=uuid4(),
            user_id=uuid4(),
            un_number="1203",
            imdg_class="3",
            name="Petrol",
            aliases=["1203"],
            adr_tunnel_code="D",
            segregation_group="none",
            packing_group="II",
            marine_pollutant=False,
            limited_quantity=False,
        )


@pytest.mark.asyncio
async def test_create_rejects_token_already_in_catalog() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[None, _row(un_number="1203")])
    service = DangerousGoodService(session)
    with pytest.raises(DangerousGoodConflict, match="1203"):
        await service.create_good(
            organization_id=uuid4(),
            user_id=uuid4(),
            un_number="1263",
            imdg_class="3",
            name="Paint",
            aliases=["1203"],
            adr_tunnel_code="D",
            segregation_group="none",
            packing_group="II",
            marine_pollutant=False,
            limited_quantity=False,
        )


@pytest.mark.asyncio
async def test_resolve_returns_catalog_row_for_alias() -> None:
    session = AsyncMock()
    row = _row(un_number="1203", aliases=["1213"])
    session.scalar = AsyncMock(return_value=row)
    service = DangerousGoodService(session)

    found = await service.resolve("UN1213")
    assert found.un_number == "1203"


@pytest.mark.asyncio
async def test_resolve_rejects_unknown_loose_string() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = DangerousGoodService(session)
    with pytest.raises(UnknownDangerousGood, match="9999"):
        await service.resolve("9999")


@pytest.mark.asyncio
async def test_list_goods_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _row(un_number="1203")
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = DangerousGoodService(session)

    listed = await service.list_goods()
    assert listed == [row]
