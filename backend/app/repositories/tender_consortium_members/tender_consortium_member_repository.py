from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_consortium_member import TenderConsortiumMember


class TenderConsortiumMemberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_seats(self) -> list[TenderConsortiumMember]:
        result = await self._session.scalars(
            select(TenderConsortiumMember).order_by(
                TenderConsortiumMember.created_at.desc(),
                TenderConsortiumMember.id,
            ),
        )
        return list(result.all())

    async def add(self, row: TenderConsortiumMember) -> TenderConsortiumMember:
        self._session.add(row)
        await self._session.flush()
        return row
