from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charge_code import ChargeCode


class ChargeCodeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[ChargeCode]:
        result = await self._session.scalars(select(ChargeCode).order_by(ChargeCode.code))
        return list(result.all())

    async def find_by_token(self, token: str) -> ChargeCode | None:
        stmt = select(ChargeCode).where(
            or_(ChargeCode.code == token, ChargeCode.aliases.contains([token])),
        )
        found = await self._session.scalar(stmt)
        return found if isinstance(found, ChargeCode) else None

    async def add(self, row: ChargeCode) -> ChargeCode:
        self._session.add(row)
        await self._session.flush()
        return row
