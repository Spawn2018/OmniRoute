from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.network import Network


class NetworkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Network]:
        result = await self._session.scalars(select(Network).order_by(Network.code))
        return list(result.all())

    async def find_by_token(self, token: str) -> Network | None:
        stmt = select(Network).where(
            or_(Network.code == token, Network.aliases.contains([token])),
        )
        found = await self._session.scalar(stmt)
        return found if isinstance(found, Network) else None

    async def add(self, row: Network) -> Network:
        self._session.add(row)
        await self._session.flush()
        return row
