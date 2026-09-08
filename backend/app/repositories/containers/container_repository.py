from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.container import Container


class ContainerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current(self, iso_size_type: str | None) -> list[Container]:
        stmt = select(Container).where(Container.superseded_by.is_(None))
        if iso_size_type is not None:
            stmt = stmt.where(Container.iso_size_type == iso_size_type)
        result = await self._session.scalars(
            stmt.order_by(Container.container_no, Container.id),
        )
        return list(result.all())

    async def find_current(self, container_no: str) -> Container | None:
        result = await self._session.scalars(
            select(Container).where(
                Container.container_no == container_no,
                Container.superseded_by.is_(None),
            ),
        )
        found = list(result.all())
        return found[0] if found else None

    async def add(self, row: Container) -> Container:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(self, current: Container, successor_id: UUID) -> Container:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
