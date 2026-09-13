from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.outcome_ledger import OutcomeLedgerDraft, parse_outcome_ledger_row
from app.models.outcome_ledger import OutcomeLedger
from app.repositories.outcome_ledgers.outcome_ledger_repository import (
    OutcomeLedgerRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: OutcomeLedgerDraft,
) -> OutcomeLedger:
    return OutcomeLedger(
        id=uuid4(),
        organization_id=organization_id,
        target_bc=draft.target_bc,
        entity_id=draft.entity_id,
        suggestion_id=draft.suggestion_id,
        outcome_kind=draft.outcome_kind,
        actual_value=draft.actual_value,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class OutcomeLedgerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OutcomeLedgerRepository(session)

    async def list_rows(self) -> list[OutcomeLedger]:
        return await self._rows.list_rows()

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        target_bc: object,
        entity_id: object,
        suggestion_id: object,
        outcome_kind: object,
        actual_value: object,
        source_ref: object,
    ) -> OutcomeLedger:
        draft = parse_outcome_ledger_row(
            target_bc,
            entity_id,
            suggestion_id,
            outcome_kind,
            actual_value,
            source_ref,
        )
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
