from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidFxDifference
from app.domain.fx_difference import (
    require_fx_quotation_id,
    require_fx_rate_id,
    require_fx_source_ref,
)
from app.models.fx_difference import FxDifference
from app.repositories.fx_differences.fx_difference_repository import FxDifferenceRepository


class FxDifferenceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FxDifferenceRepository(session)

    async def list_differences(self) -> list[FxDifference]:
        return await self._rows.list_all()

    async def record_difference(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        nbp_rate_id: UUID,
        source_ref: str,
    ) -> FxDifference:
        row = FxDifference(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=require_fx_quotation_id(quotation_id),
            nbp_rate_id=require_fx_rate_id(nbp_rate_id),
            source_ref=require_fx_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidFxDifference("para już zapisana") from orig
