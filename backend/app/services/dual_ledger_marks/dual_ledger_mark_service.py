from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dual_ledger_mark import parse_dual_ledger_mark_row
from app.models.dual_ledger_mark import DualLedgerMark
from app.repositories.dual_ledger_marks.dual_ledger_mark_repository import (
    DualLedgerMarkRepository,
)


class DualLedgerMarkService:
    """HITL katalog dual ledger — bez drugiej marży i bez SQL na charge."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = DualLedgerMarkRepository(session)

    async def list_marks(self) -> list[DualLedgerMark]:
        return await self._marks.list_marks()

    async def persist_dual_ledger_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ledger_kind: object,
        source_ref: object,
    ) -> DualLedgerMark:
        code, kind, pointer = parse_dual_ledger_mark_row(
            mark_code,
            ledger_kind,
            source_ref,
        )
        row = DualLedgerMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ledger_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
