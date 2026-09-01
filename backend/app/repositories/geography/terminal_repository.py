from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terminal import Terminal


class TerminalRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(
        self,
        *,
        port_id: UUID | None = None,
        search: str | None = None,
    ) -> list[Terminal]:
        stmt = select(Terminal).order_by(Terminal.name)
        if port_id is not None:
            stmt = stmt.where(Terminal.port_id == port_id)
        token = "" if search is None else search.strip().upper()
        if token != "":
            pattern = f"%{token}%"
            stmt = stmt.where(
                or_(
                    func.upper(Terminal.name).like(pattern),
                    Terminal.isps_code.like(pattern),
                ),
            )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def find_by_isps(self, isps_code: str) -> Terminal | None:
        found = await self._session.scalar(
            select(Terminal).where(Terminal.isps_code == isps_code),
        )
        return found if isinstance(found, Terminal) else None

    async def add(self, row: Terminal) -> Terminal:
        self._session.add(row)
        await self._session.flush()
        return row
