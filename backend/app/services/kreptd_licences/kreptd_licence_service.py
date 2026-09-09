from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.kreptd_licence import (
    require_kreptd_source_ref,
    require_licence_no,
    require_party_id,
)
from app.models.kreptd_licence import KreptdLicence
from app.repositories.kreptd_licences.kreptd_licence_repository import (
    KreptdLicenceRepository,
)


class KreptdLicenceService:
    def __init__(self, session: AsyncSession) -> None:
        self._licences = KreptdLicenceRepository(session)

    async def list_licences(self) -> list[KreptdLicence]:
        return await self._licences.fetch_licences()

    async def persist_licence(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: object,
        licence_no: object,
        source_ref: object,
    ) -> KreptdLicence:
        row = KreptdLicence(
            id=uuid4(),
            organization_id=organization_id,
            party_id=require_party_id(party_id),
            licence_no=require_licence_no(licence_no),
            source_ref=require_kreptd_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._licences.add(row)
