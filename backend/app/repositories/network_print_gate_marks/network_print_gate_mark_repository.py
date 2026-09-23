from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.network_print_gate_mark import NetworkPrintGateMark


class NetworkPrintGateMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[NetworkPrintGateMark]:
        result = await self._db.scalars(
            select(NetworkPrintGateMark).order_by(
                NetworkPrintGateMark.gate_kind.asc(),
                NetworkPrintGateMark.mark_code.asc(),
                NetworkPrintGateMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: NetworkPrintGateMark) -> NetworkPrintGateMark:
        self._db.add(row)
        await self._db.flush()
        return row
