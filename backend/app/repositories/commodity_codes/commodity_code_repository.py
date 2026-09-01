from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.commodity_code import CommodityCode


class CommodityCodeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CommodityCode]:
        result = await self._session.scalars(select(CommodityCode).order_by(CommodityCode.code))
        return list(result.all())

    async def find_by_token(self, token: str) -> CommodityCode | None:
        stmt = select(CommodityCode).where(
            or_(CommodityCode.code == token, CommodityCode.aliases.contains([token])),
        )
        found = await self._session.scalar(stmt)
        return found if isinstance(found, CommodityCode) else None

    async def add(self, row: CommodityCode) -> CommodityCode:
        self._session.add(row)
        await self._session.flush()
        return row
