from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice_match_candidate import InvoiceMatchCandidate


class InvoiceMatchCandidateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[InvoiceMatchCandidate]:
        packed = await self._session.scalars(
            select(InvoiceMatchCandidate).order_by(
                InvoiceMatchCandidate.candidate_code,
                InvoiceMatchCandidate.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: InvoiceMatchCandidate) -> InvoiceMatchCandidate:
        self._session.add(row)
        await self._session.flush()
        return row
