from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import InvalidNetworkCode, NetworkConflict, UnknownNetwork
from app.models.network import Network
from app.services.networks.network_service import NetworkService


def _row(*, code: str, aliases: list[str] | None = None) -> Network:
    return Network(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=aliases or [],
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_normalizes_code_and_optional_fields() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = NetworkService(session)

    created = await service.create_network(
        organization_id=uuid4(),
        user_id=uuid4(),
        code=" WCA ",
        name=" WCA Worldwide ",
        aliases=[" wca_ww "],
        website=" https://wca.com ",
        region_scope="  ",
        is_global=True,
    )

    assert created.code == "wca"
    assert created.name == "WCA Worldwide"
    assert created.aliases == ["wca_ww"]
    assert created.website == "https://wca.com"
    assert created.region_scope is None
    assert created.is_global is True
    assert created.source_ref == "tenant:manual"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_blank_name() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = NetworkService(session)
    with pytest.raises(InvalidNetworkCode, match="nazwa"):
        await service.create_network(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="wca",
            name="   ",
            aliases=[],
            website=None,
            region_scope=None,
            is_global=False,
        )


@pytest.mark.asyncio
async def test_create_rejects_alias_equal_to_code() -> None:
    service = NetworkService(AsyncMock())
    with pytest.raises(InvalidNetworkCode, match="alias"):
        await service.create_network(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="wca",
            name="WCA",
            aliases=["WCA"],
            website=None,
            region_scope=None,
            is_global=True,
        )


@pytest.mark.asyncio
async def test_create_rejects_token_already_in_catalog() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[None, _row(code="wca")])
    service = NetworkService(session)
    with pytest.raises(NetworkConflict, match="wca"):
        await service.create_network(
            organization_id=uuid4(),
            user_id=uuid4(),
            code="fiata",
            name="FIATA",
            aliases=["wca"],
            website=None,
            region_scope=None,
            is_global=True,
        )


@pytest.mark.asyncio
async def test_resolve_returns_catalog_row_for_alias() -> None:
    session = AsyncMock()
    row = _row(code="wca", aliases=["wca_ww"])
    session.scalar = AsyncMock(return_value=row)
    service = NetworkService(session)

    found = await service.resolve("wca_ww")
    assert found.code == "wca"


@pytest.mark.asyncio
async def test_resolve_rejects_unknown_token() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = NetworkService(session)
    with pytest.raises(UnknownNetwork, match="xyz"):
        await service.resolve("xyz")
