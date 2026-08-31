from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table_view import TableView


class TableViewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_owner(self, user_id: UUID, table_key: str) -> list[TableView]:
        result = await self._session.scalars(
            select(TableView)
            .where(TableView.user_id == user_id, TableView.table_key == table_key)
            .order_by(TableView.name),
        )
        return list(result.all())

    async def get_by_id(self, view_id: UUID) -> TableView | None:
        return await self._session.get(TableView, view_id)

    async def add(self, view: TableView) -> TableView:
        self._session.add(view)
        await self._session.flush()
        return view

    async def delete(self, view: TableView) -> None:
        await self._session.delete(view)
        await self._session.flush()
