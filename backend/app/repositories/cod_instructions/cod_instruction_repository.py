from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cod_instruction import CodInstruction


class CodInstructionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CodInstruction]:
        result = await self._session.scalars(
            select(CodInstruction).order_by(
                CodInstruction.created_at.desc(),
                CodInstruction.id,
            ),
        )
        return list(result.all())

    async def add(self, row: CodInstruction) -> CodInstruction:
        self._session.add(row)
        await self._session.flush()
        return row
