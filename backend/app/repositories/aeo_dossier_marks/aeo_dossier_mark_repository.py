from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aeo_dossier_mark import AeoDossierMark


class AeoDossierMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[AeoDossierMark]:
        packed = await self._session.scalars(
            select(AeoDossierMark).order_by(
                AeoDossierMark.mark_code,
                AeoDossierMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: AeoDossierMark) -> AeoDossierMark:
        self._session.add(row)
        await self._session.flush()
        return row
