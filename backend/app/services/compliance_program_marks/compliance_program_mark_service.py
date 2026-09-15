from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.compliance_program_mark import parse_compliance_program_mark_row
from app.models.compliance_program_mark import ComplianceProgramMark
from app.repositories.compliance_program_marks.compliance_program_mark_repository import (
    ComplianceProgramMarkRepository,
)


class ComplianceProgramMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ComplianceProgramMarkRepository(session)

    async def list_marks(self) -> list[ComplianceProgramMark]:
        return await self._rows.list_marks()

    async def persist_compliance_program_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        program_kind: object,
        source_ref: object,
    ) -> ComplianceProgramMark:
        code, kind, origin = parse_compliance_program_mark_row(
            mark_code,
            program_kind,
            source_ref,
        )
        row = ComplianceProgramMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            program_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
