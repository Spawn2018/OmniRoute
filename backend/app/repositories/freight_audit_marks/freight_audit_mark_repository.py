from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.freight_audit_mark import FreightAuditMark


class FreightAuditMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FreightAuditMark]:
        packed = await self._session.scalars(
            select(FreightAuditMark).order_by(
                FreightAuditMark.mark_code, FreightAuditMark.id
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FreightAuditMark) -> FreightAuditMark:
        self._session.add(row)
        await self._session.flush()
        return row
