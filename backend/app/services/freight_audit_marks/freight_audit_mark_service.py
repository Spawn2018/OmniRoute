from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.freight_audit_mark import parse_freight_audit_mark_row
from app.models.freight_audit_mark import FreightAuditMark
from app.repositories.freight_audit_marks.freight_audit_mark_repository import (
    FreightAuditMarkRepository,
)


class FreightAuditMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FreightAuditMarkRepository(session)

    async def list_marks(self) -> list[FreightAuditMark]:
        return await self._rows.list_marks()

    async def persist_freight_audit_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        audit_kind: object,
        source_ref: object,
    ) -> FreightAuditMark:
        code, kind, origin = parse_freight_audit_mark_row(
            mark_code, audit_kind, source_ref
        )
        row = FreightAuditMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            audit_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
