from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.compliance_program_mark import ComplianceProgramMark


class ComplianceProgramMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ComplianceProgramMark]:
        stmt = select(ComplianceProgramMark).order_by(
            ComplianceProgramMark.mark_code,
            ComplianceProgramMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: ComplianceProgramMark) -> ComplianceProgramMark:
        self._session.add(row)
        await self._session.flush()
        return row
