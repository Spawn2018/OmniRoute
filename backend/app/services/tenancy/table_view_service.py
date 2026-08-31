from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.models.table_view import TableView
from app.repositories.tenancy.table_view_repository import TableViewRepository


class TableViewService:
    def __init__(self, session: AsyncSession) -> None:
        self._views = TableViewRepository(session)
        self._session = session

    async def list_views(self, user_id: UUID, table_key: str) -> list[TableView]:
        return await self._views.list_for_owner(user_id, table_key)

    async def create_view(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        table_key: str,
        name: str,
        config: dict[str, Any],
    ) -> TableView:
        view = TableView(
            id=uuid4(),
            organization_id=organization_id,
            user_id=user_id,
            table_key=table_key,
            name=name.strip(),
            config=config,
            created_by=user_id,
        )
        return await self._views.add(view)

    async def update_view(
        self,
        *,
        view_id: UUID,
        user_id: UUID,
        name: str | None,
        config: dict[str, Any] | None,
    ) -> TableView:
        view = await self._require_owned(view_id, user_id)
        if name is not None:
            view.name = name.strip()
        if config is not None:
            view.config = config
        await self._session.flush()
        return view

    async def delete_view(self, view_id: UUID, user_id: UUID) -> None:
        view = await self._require_owned(view_id, user_id)
        await self._views.delete(view)

    async def _require_owned(self, view_id: UUID, user_id: UUID) -> TableView:
        view = await self._views.get_by_id(view_id)
        if view is None or view.user_id != user_id:
            raise ResourceNotFound("Widok tabeli nie istnieje")
        return view
