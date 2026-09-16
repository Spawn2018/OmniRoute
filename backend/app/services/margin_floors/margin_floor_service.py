from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.margin_floor import MarginFloorDraft, parse_margin_floor_row
from app.models.margin_floor import MarginFloor
from app.repositories.margin_floors.margin_floor_repository import MarginFloorRepository


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: MarginFloorDraft,
) -> MarginFloor:
    return MarginFloor(
        id=uuid4(),
        organization_id=organization_id,
        floor_code=draft.floor_code,
        origin_unlocode=draft.origin_unlocode,
        destination_unlocode=draft.destination_unlocode,
        floor_amount=draft.floor_amount,
        floor_currency=draft.floor_currency,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class MarginFloorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = MarginFloorRepository(session)

    async def list_rows(self) -> list[MarginFloor]:
        return await self._rows.list_rows()

    async def persist_floor(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        floor_code: object,
        origin_unlocode: object,
        destination_unlocode: object,
        floor_amount: object,
        floor_currency: object,
        source_ref: object,
    ) -> MarginFloor:
        draft = parse_margin_floor_row(
            floor_code,
            origin_unlocode,
            destination_unlocode,
            floor_amount,
            floor_currency,
            source_ref,
        )
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
