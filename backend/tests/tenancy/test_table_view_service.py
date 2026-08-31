from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import ResourceNotFound
from app.models.table_view import TableView
from app.services.tenancy.table_view_service import TableViewService


@pytest.mark.asyncio
async def test_create_and_list_table_view() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = TableViewService(session)
    org_id = uuid4()
    user_id = uuid4()

    created = await service.create_view(
        organization_id=org_id,
        user_id=user_id,
        table_key="tenancy.users",
        name=" Operacyjny ",
        config={"density": "compact"},
    )
    assert created.name == "Operacyjny"
    assert created.organization_id == org_id
    session.add.assert_called_once()
    session.flush.assert_awaited()

    row = TableView(
        id=uuid4(),
        organization_id=org_id,
        user_id=user_id,
        table_key="tenancy.users",
        name="Operacyjny",
        config={"density": "compact"},
    )
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)

    listed = await service.list_views(user_id, "tenancy.users")
    assert listed == [row]


@pytest.mark.asyncio
async def test_update_and_delete_owned_view() -> None:
    session = AsyncMock()
    session.flush = AsyncMock()
    session.delete = AsyncMock()
    view_id = uuid4()
    user_id = uuid4()
    view = TableView(
        id=view_id,
        organization_id=uuid4(),
        user_id=user_id,
        table_key="tenancy.users",
        name="Stary",
        config={},
    )
    session.get = AsyncMock(return_value=view)
    service = TableViewService(session)

    updated = await service.update_view(
        view_id=view_id,
        user_id=user_id,
        name="Nowy",
        config={"density": "comfortable"},
    )
    assert updated.name == "Nowy"
    assert updated.config["density"] == "comfortable"

    await service.delete_view(view_id, user_id)
    session.delete.assert_awaited()


@pytest.mark.asyncio
async def test_update_foreign_view_raises() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    service = TableViewService(session)
    with pytest.raises(ResourceNotFound):
        await service.update_view(view_id=uuid4(), user_id=uuid4(), name="X", config=None)
