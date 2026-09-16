from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.network_member import NetworkMember
from app.models.party import Party


class NetworkMemberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_network(
        self,
        network_id: UUID,
        *,
        country_code: str | None = None,
    ) -> list[NetworkMember]:
        stmt = (
            select(NetworkMember)
            .where(NetworkMember.network_id == network_id)
            .order_by(NetworkMember.member_code)
        )
        if country_code is not None:
            # Filtr O7: kraj z party — nie druga kolumna na network_member
            stmt = (
                stmt.join(
                    Party,
                    (Party.organization_id == NetworkMember.organization_id)
                    & (Party.id == NetworkMember.party_id),
                ).where(Party.country_code == country_code)
            )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def add(self, row: NetworkMember) -> NetworkMember:
        self._session.add(row)
        await self._session.flush()
        return row
