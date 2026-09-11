from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.billing_mark import parse_billing_mark_row
from app.models.billing_mark import BillingMark
from app.repositories.billing_marks.billing_mark_repository import BillingMarkRepository


class BillingMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BillingMarkRepository(session)

    async def list_marks(self) -> list[BillingMark]:
        return await self._rows.list_marks()

    async def persist_billing_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        billing_kind: object,
        source_ref: object,
    ) -> BillingMark:
        code, kind, origin = parse_billing_mark_row(
            mark_code,
            billing_kind,
            source_ref,
        )
        row = BillingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            billing_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
