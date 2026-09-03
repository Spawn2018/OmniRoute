from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import OperatorDecisionConflict, ResourceNotFound
from app.domain.operator_decision import (
    operator_decision_pending_status,
    require_decide_status,
    require_decision_source_ref,
    require_pending_before_decide,
    require_subject_id,
    require_subject_kind,
)
from app.models.operator_decision import OperatorDecision
from app.repositories.operator_decisions.operator_decision_repository import (
    OperatorDecisionRepository,
)


class OperatorDecisionService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OperatorDecisionRepository(session)

    async def list_decisions(self) -> list[OperatorDecision]:
        return await self._rows.list_all()

    async def get_decision(self, decision_id: UUID) -> OperatorDecision:
        found = await self._rows.get(decision_id)
        if found is None:
            raise ResourceNotFound(f"nieznana decyzja operatora: {decision_id}")
        return found

    async def create_decision(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_kind: str,
        subject_id: UUID,
        source_ref: str,
    ) -> OperatorDecision:
        row = OperatorDecision(
            id=uuid4(),
            organization_id=organization_id,
            subject_kind=require_subject_kind(subject_kind),
            subject_id=require_subject_id(subject_id),
            status=operator_decision_pending_status(),
            source_ref=require_decision_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            detail = str(orig.orig) if orig.orig is not None else str(orig)
            if "uq_operator_decision_pending" in detail:
                raise OperatorDecisionConflict(
                    "pending na ten subject już istnieje",
                ) from orig
            raise

    async def decide(self, decision_id: UUID, status: str) -> OperatorDecision:
        row = await self.get_decision(decision_id)
        require_pending_before_decide(row.status)
        row.status = require_decide_status(status)
        row.decided_at = datetime.now(UTC)
        return await self._rows.save(row)
