from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource import Resource


class ResourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, resource_id: UUID) -> Resource | None:
        return await self._session.get(Resource, resource_id)

    async def list_current(self, resource_kind: str | None) -> list[Resource]:
        stmt = select(Resource).where(Resource.superseded_by.is_(None))
        if resource_kind is not None:
            stmt = stmt.where(Resource.resource_kind == resource_kind)
        result = await self._session.scalars(
            stmt.order_by(Resource.resource_kind, Resource.display_name, Resource.id),
        )
        return list(result.all())

    async def find_current(self, resource_kind: str, display_name: str) -> Resource | None:
        result = await self._session.scalars(
            select(Resource).where(
                Resource.resource_kind == resource_kind,
                Resource.display_name == display_name,
                Resource.superseded_by.is_(None),
            ),
        )
        found = list(result.all())
        return found[0] if found else None

    async def add(self, row: Resource) -> Resource:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(self, current: Resource, successor_id: UUID) -> Resource:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
