from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.suggestion_ledger import SuggestionLedgerDraft, parse_suggestion_ledger_row
from app.models.suggestion_ledger import SuggestionLedger
from app.repositories.suggestion_ledgers.suggestion_ledger_repository import (
    SuggestionLedgerRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: SuggestionLedgerDraft,
) -> SuggestionLedger:
    return SuggestionLedger(
        id=uuid4(),
        organization_id=organization_id,
        target_bc=draft.target_bc,
        entity_id=draft.entity_id,
        suggestion_kind=draft.suggestion_kind,
        interval_low=draft.interval_low,
        interval_high=draft.interval_high,
        model_version=draft.model_version,
        prompt_version=draft.prompt_version,
        reaction=draft.reaction,
        changed_to=draft.changed_to,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class SuggestionLedgerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SuggestionLedgerRepository(session)

    async def list_rows(self) -> list[SuggestionLedger]:
        return await self._rows.list_rows()

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        target_bc: object,
        entity_id: object,
        suggestion_kind: object,
        interval_low: object,
        interval_high: object,
        model_version: object,
        prompt_version: object,
        reaction: object,
        changed_to: object,
        source_ref: object,
    ) -> SuggestionLedger:
        draft = parse_suggestion_ledger_row(
            target_bc,
            entity_id,
            suggestion_kind,
            interval_low,
            interval_high,
            model_version,
            prompt_version,
            reaction,
            changed_to,
            source_ref,
        )
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
