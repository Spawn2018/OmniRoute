from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charge_template import ChargeTemplate


class ChargeTemplateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[ChargeTemplate]:
        result = await self._session.scalars(
            select(ChargeTemplate).order_by(ChargeTemplate.created_at.desc(), ChargeTemplate.id),
        )
        return list(result.all())

    async def add(self, row: ChargeTemplate) -> ChargeTemplate:
        self._session.add(row)
        await self._session.flush()
        return row
