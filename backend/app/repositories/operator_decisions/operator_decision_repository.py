from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operator_decision import OperatorDecision


class OperatorDecisionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[OperatorDecision]:
        result = await self._session.scalars(
            select(OperatorDecision).order_by(OperatorDecision.created_at.desc()),
        )
        return list(result.all())

    async def get(self, decision_id: UUID) -> OperatorDecision | None:
        found = await self._session.get(OperatorDecision, decision_id)
        return found if isinstance(found, OperatorDecision) else None

    async def add(self, row: OperatorDecision) -> OperatorDecision:
        self._session.add(row)
        await self._session.flush()
        return row

    async def save(self, row: OperatorDecision) -> OperatorDecision:
        await self._session.flush()
        return row
