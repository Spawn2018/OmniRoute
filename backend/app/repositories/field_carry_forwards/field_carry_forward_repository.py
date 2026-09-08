from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.field_carry_forward import FieldCarryForward


class FieldCarryForwardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_shipment(self, shipment_id: UUID) -> list[FieldCarryForward]:
        result = await self._session.scalars(
            select(FieldCarryForward)
            .where(FieldCarryForward.shipment_id == shipment_id)
            .order_by(FieldCarryForward.created_at.desc(), FieldCarryForward.id),
        )
        return list(result.all())

    async def find_current(
        self,
        quotation_id: UUID,
        shipment_id: UUID,
        field_key: str,
    ) -> FieldCarryForward | None:
        result = await self._session.scalars(
            select(FieldCarryForward).where(
                FieldCarryForward.quotation_id == quotation_id,
                FieldCarryForward.shipment_id == shipment_id,
                FieldCarryForward.field_key == field_key,
                FieldCarryForward.superseded_by.is_(None),
            ),
        )
        found = result.first()
        return found if isinstance(found, FieldCarryForward) else None

    async def add(self, row: FieldCarryForward) -> FieldCarryForward:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(
        self,
        current: FieldCarryForward,
        successor_id: UUID,
    ) -> FieldCarryForward:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
