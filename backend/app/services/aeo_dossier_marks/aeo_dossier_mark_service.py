from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.aeo_dossier_mark import parse_aeo_dossier_mark_row
from app.models.aeo_dossier_mark import AeoDossierMark
from app.repositories.aeo_dossier_marks.aeo_dossier_mark_repository import AeoDossierMarkRepository


class AeoDossierMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = AeoDossierMarkRepository(session)

    async def list_marks(self) -> list[AeoDossierMark]:
        return await self._rows.list_marks()

    async def persist_aeo_dossier_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        dossier_kind: object,
        source_ref: object,
    ) -> AeoDossierMark:
        code, kind, origin = parse_aeo_dossier_mark_row(
            mark_code,
            dossier_kind,
            source_ref,
        )
        row = AeoDossierMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            dossier_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
