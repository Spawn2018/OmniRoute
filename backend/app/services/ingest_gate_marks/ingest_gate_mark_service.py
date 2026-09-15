from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ingest_gate_mark import parse_ingest_gate_mark_row
from app.models.ingest_gate_mark import IngestGateMark
from app.repositories.ingest_gate_marks.ingest_gate_mark_repository import (
    IngestGateMarkRepository,
)


class IngestGateMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = IngestGateMarkRepository(session)

    async def list_marks(self) -> list[IngestGateMark]:
        return await self._rows.list_marks()

    async def persist_ingest_gate_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        gate_kind: object,
        source_ref: object,
    ) -> IngestGateMark:
        code, kind, origin = parse_ingest_gate_mark_row(
            mark_code,
            gate_kind,
            source_ref,
        )
        row = IngestGateMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            gate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
