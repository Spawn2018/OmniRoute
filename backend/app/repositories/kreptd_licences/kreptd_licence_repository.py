from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.kreptd_licence import KreptdLicence


class KreptdLicenceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_licences(self) -> list[KreptdLicence]:
        packed = await self._session.scalars(
            select(KreptdLicence).order_by(
                KreptdLicence.created_at.desc(),
                KreptdLicence.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: KreptdLicence) -> KreptdLicence:
        self._session.add(row)
        await self._session.flush()
        return row
