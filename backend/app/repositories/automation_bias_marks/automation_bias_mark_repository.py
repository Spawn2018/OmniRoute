from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.automation_bias_mark import AutomationBiasMark


class AutomationBiasMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[AutomationBiasMark]:
        stmt = select(AutomationBiasMark).order_by(
            AutomationBiasMark.mark_code,
            AutomationBiasMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: AutomationBiasMark) -> AutomationBiasMark:
        self._session.add(row)
        await self._session.flush()
        return row
