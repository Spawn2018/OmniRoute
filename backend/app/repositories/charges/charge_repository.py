from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date as SqlDate
from sqlalchemy import bindparam, select, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charge import Charge, ShipmentTreeMargin

# T7d: mnożenie mid w Postgres — HC-11, nie float w Pythonie.
_SELL_IN_PLN = text(
    "SELECT charge_sell_in_pln(:charge_id, CAST(:on_date AS date))",
).bindparams(
    bindparam("charge_id", type_=PGUUID(as_uuid=True)),
    bindparam("on_date", type_=SqlDate),
)


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

    async def sell_in_pln(self, charge_id: UUID, on_date: object) -> Decimal | None:
        raw = await self._session.scalar(
            _SELL_IN_PLN,
            {"charge_id": charge_id, "on_date": on_date},
        )
        if raw is None:
            return None
        return Decimal(str(raw))

    async def add(self, row: Charge) -> Charge:
        self._session.add(row)
        await self._session.flush()
        return row
