from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.benefit_ledger import BenefitLedgerDraft, parse_benefit_ledger_row
from app.models.benefit_ledger import BenefitLedger
from app.repositories.benefit_ledgers.benefit_ledger_repository import (
    BenefitLedgerRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: BenefitLedgerDraft,
) -> BenefitLedger:
    return BenefitLedger(
        id=uuid4(),
        organization_id=organization_id,
        benefit_code=draft.benefit_code,
        method_label=draft.method_label,
        hours_saved=draft.hours_saved,
        saved_amount=draft.saved_amount,
        saved_currency=draft.saved_currency,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class BenefitLedgerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BenefitLedgerRepository(session)

    async def list_rows(self) -> list[BenefitLedger]:
        return await self._rows.list_rows()

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        benefit_code: object,
        method_label: object,
        hours_saved: object,
        saved_amount: object,
        saved_currency: object,
        source_ref: object,
    ) -> BenefitLedger:
        draft = parse_benefit_ledger_row(
            benefit_code,
            method_label,
            hours_saved,
            saved_amount,
            saved_currency,
            source_ref,
        )
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
