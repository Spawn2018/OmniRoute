from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.network_member import NetworkMember


class NetworkMemberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_network(self, network_id: UUID) -> list[NetworkMember]:
        result = await self._session.scalars(
            select(NetworkMember)
            .where(NetworkMember.network_id == network_id)
            .order_by(NetworkMember.member_code),
        )
        return list(result.all())

    async def add(self, row: NetworkMember) -> NetworkMember:
        self._session.add(row)
        await self._session.flush()
        return row
