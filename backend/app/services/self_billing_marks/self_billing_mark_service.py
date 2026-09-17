from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.self_billing_mark import parse_self_billing_mark_row
from app.models.self_billing_mark import SelfBillingMark
from app.repositories.self_billing_marks.self_billing_mark_repository import (
    SelfBillingMarkRepository,
)


class SelfBillingMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SelfBillingMarkRepository(session)

    async def list_marks(self) -> list[SelfBillingMark]:
        return await self._rows.list_marks()

    async def persist_self_billing_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        billing_kind: object,
        source_ref: object,
    ) -> SelfBillingMark:
        code, kind, origin = parse_self_billing_mark_row(
            mark_code,
            billing_kind,
            source_ref,
        )
        row = SelfBillingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            billing_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
