from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.groupage_tariff import GroupageTariff


class GroupageTariffRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[GroupageTariff]:
        result = await self._session.scalars(
            select(GroupageTariff).order_by(
                GroupageTariff.created_at.desc(),
                GroupageTariff.id,
            ),
        )
        return list(result.all())

    async def add(self, row: GroupageTariff) -> GroupageTariff:
        self._session.add(row)
        await self._session.flush()
        return row
