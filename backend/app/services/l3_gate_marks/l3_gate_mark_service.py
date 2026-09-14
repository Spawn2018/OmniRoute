from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.l3_gate_mark import parse_l3_gate_mark_row
from app.models.l3_gate_mark import L3GateMark
from app.repositories.l3_gate_marks.l3_gate_mark_repository import (
    L3GateMarkRepository,
)


class L3GateMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = L3GateMarkRepository(session)

    async def list_marks(self) -> list[L3GateMark]:
        return await self._rows.list_marks()

    async def persist_l3_gate_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        gate_kind: object,
        source_ref: object,
    ) -> L3GateMark:
        code, kind, origin = parse_l3_gate_mark_row(
            mark_code,
            gate_kind,
            source_ref,
        )
        row = L3GateMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            gate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
