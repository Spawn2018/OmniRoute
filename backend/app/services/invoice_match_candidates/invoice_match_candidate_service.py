from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.invoice_match_candidate import parse_invoice_match_candidate_row
from app.models.invoice_match_candidate import InvoiceMatchCandidate
from app.repositories.invoice_match_candidates import (
    InvoiceMatchCandidateRepository,
)


class InvoiceMatchCandidateService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = InvoiceMatchCandidateRepository(session)

    async def list_marks(self) -> list[InvoiceMatchCandidate]:
        return await self._rows.list_marks()

    async def persist_invoice_match_candidate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        candidate_code: object,
        candidate_kind: object,
        source_ref: object,
    ) -> InvoiceMatchCandidate:
        code, kind, origin = parse_invoice_match_candidate_row(
            candidate_code,
            candidate_kind,
            source_ref,
        )
        row = InvoiceMatchCandidate(
            id=uuid4(),
            organization_id=organization_id,
            candidate_code=code,
            candidate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
