from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charge import Charge, ShipmentTreeMargin


class ChargeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_with_sql_margin(self) -> list[tuple[Charge, Decimal]]:
        # HC-11: różnica sell−buy w Postgres, nie pętla margin() na GET.
        gap = (Charge.sell_amount - Charge.buy_amount).label("sql_margin")
        result = await self._session.execute(
            select(Charge, gap).order_by(Charge.created_at.desc(), Charge.id),
        )
        listed: list[tuple[Charge, Decimal]] = []
        for row, sql_margin in result.all():
            listed.append((row, Decimal(str(sql_margin))))
        return listed

    async def list_tree_margins(self) -> list[ShipmentTreeMargin]:
        loaded = await self._session.scalars(
            select(ShipmentTreeMargin).order_by(
                ShipmentTreeMargin.shipment_id,
                ShipmentTreeMargin.currency,
            ),
        )
        return list(loaded.all())

    async def get(self, charge_id: UUID) -> Charge | None:
        found = await self._session.get(Charge, charge_id)
        return found if isinstance(found, Charge) else None

    async def add(self, row: Charge) -> Charge:
        self._session.add(row)
        await self._session.flush()
        return row
