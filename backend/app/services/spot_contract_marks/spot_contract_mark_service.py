from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.spot_contract_mark import parse_spot_contract_mark_row
from app.models.spot_contract_mark import SpotContractMark
from app.repositories.spot_contract_marks.spot_contract_mark_repository import (
    SpotContractMarkRepository,
)


class SpotContractMarkService:
    """HITL katalog spot/contract — bez FK quotation i bez cargo_value."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = SpotContractMarkRepository(session)

    async def list_marks(self) -> list[SpotContractMark]:
        return await self._marks.list_marks()

    async def persist_spot_contract_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        deal_kind: object,
        source_ref: object,
    ) -> SpotContractMark:
        code, kind, pointer = parse_spot_contract_mark_row(
            mark_code,
            deal_kind,
            source_ref,
        )
        row = SpotContractMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            deal_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
