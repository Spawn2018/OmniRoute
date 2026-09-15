from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ingest_gate_mark import IngestGateMark


class IngestGateMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[IngestGateMark]:
        stmt = select(IngestGateMark).order_by(
            IngestGateMark.mark_code,
            IngestGateMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: IngestGateMark) -> IngestGateMark:
        self._session.add(row)
        await self._session.flush()
        return row
