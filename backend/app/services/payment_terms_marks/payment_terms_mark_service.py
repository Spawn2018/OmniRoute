from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.payment_terms_mark import parse_payment_terms_mark_row
from app.models.payment_terms_mark import PaymentTermsMark
from app.repositories.payment_terms_marks.payment_terms_mark_repository import (
    PaymentTermsMarkRepository,
)


class PaymentTermsMarkService:
    """HITL katalog warunków płatności — bez kolumny shipment i bez payment_terms_days."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = PaymentTermsMarkRepository(session)

    async def list_marks(self) -> list[PaymentTermsMark]:
        return await self._marks.list_marks()

    async def persist_payment_terms_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        terms_kind: object,
        source_ref: object,
    ) -> PaymentTermsMark:
        code, kind, pointer = parse_payment_terms_mark_row(
            mark_code,
            terms_kind,
            source_ref,
        )
        row = PaymentTermsMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            terms_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
