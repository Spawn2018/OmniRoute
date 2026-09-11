from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.company_mark import parse_company_mark_row
from app.models.company_mark import CompanyMark
from app.repositories.company_marks.company_mark_repository import CompanyMarkRepository


class CompanyMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CompanyMarkRepository(session)

    async def list_marks(self) -> list[CompanyMark]:
        return await self._rows.list_marks()

    async def persist_company_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        seat_kind: object,
        source_ref: object,
    ) -> CompanyMark:
        code, kind, origin = parse_company_mark_row(
            mark_code,
            seat_kind,
            source_ref,
        )
        row = CompanyMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            seat_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
