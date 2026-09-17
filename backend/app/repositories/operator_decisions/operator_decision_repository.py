from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
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

    async def get_accepted(
        self,
        subject_kind: str,
        subject_id: UUID,
    ) -> OperatorDecision | None:
        found = await self._session.scalar(
            select(OperatorDecision).where(
                OperatorDecision.subject_kind == subject_kind,
                OperatorDecision.subject_id == subject_id,
                OperatorDecision.status == "accepted",
            ),
        )
        return found if isinstance(found, OperatorDecision) else None

    async def get_pending(
        self,
        subject_kind: str,
        subject_id: UUID,
    ) -> OperatorDecision | None:
        found = await self._session.scalar(
            select(OperatorDecision).where(
                OperatorDecision.subject_kind == subject_kind,
                OperatorDecision.subject_id == subject_id,
                OperatorDecision.status == "pending",
            ),
        )
        return found if isinstance(found, OperatorDecision) else None

    async def add(self, row: OperatorDecision) -> OperatorDecision:
        self._session.add(row)
        await self._session.flush()
        return row

    async def save(self, row: OperatorDecision) -> OperatorDecision:
        await self._session.flush()
        return row

    async def claim_pending(
        self,
        *,
        decision_id: UUID,
        lock_version: int,
        status: str,
        decided_at: datetime,
    ) -> OperatorDecision | None:
        found = await self._session.scalar(
            update(OperatorDecision)
            .where(
                OperatorDecision.id == decision_id,
                OperatorDecision.status == "pending",
                OperatorDecision.lock_version == lock_version,
            )
            .values(
                status=status,
                lock_version=lock_version + 1,
                decided_at=decided_at,
            )
            .returning(OperatorDecision),
        )
        return found if isinstance(found, OperatorDecision) else None
