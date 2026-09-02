from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.port import Port
from app.models.port_surcharge import PortSurcharge


class PortSurchargeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[PortSurcharge]:
        result = await self._session.scalars(select(PortSurcharge).order_by(PortSurcharge.title))
        return list(result.all())

    async def get_port(self, port_id: UUID) -> Port | None:
        found = await self._session.scalar(select(Port).where(Port.id == port_id))
        return found if isinstance(found, Port) else None

    async def list_matching(self, port_id: UUID, applies_when: str) -> list[PortSurcharge]:
        result = await self._session.scalars(
            select(PortSurcharge)
            .where(
                PortSurcharge.port_id == port_id,
                PortSurcharge.applies_when == applies_when,
            )
            .order_by(PortSurcharge.title),
        )
        return list(result.all())

    async def find_by_port_and_code(self, port_id: UUID, code: str) -> PortSurcharge | None:
        found = await self._session.scalar(
            select(PortSurcharge).where(
                PortSurcharge.port_id == port_id,
                PortSurcharge.code == code,
            ),
        )
        return found if isinstance(found, PortSurcharge) else None

    async def add(self, row: PortSurcharge) -> PortSurcharge:
        self._session.add(row)
        await self._session.flush()
        return row
