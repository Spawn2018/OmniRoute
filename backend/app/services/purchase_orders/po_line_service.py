from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.po_line import parse_po_line_row
from app.models.po_line import PoLine
from app.repositories.purchase_orders.po_line_repository import PoLineRepository

_PoLineParsed = tuple[
    UUID, str, str, Decimal, str, str | None, str | None, str | None, str | None, str
]


class PoLineService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PoLineRepository(session)

    async def list_lines(self) -> list[PoLine]:
        return await self._rows.list_lines()

    async def persist_po_line(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        purchase_order_id: object,
        line_code: object,
        sku_code: object,
        qty: object,
        uom_code: object,
        plant_label: object,
        batch_label: object,
        serial_label: object,
        coo_label: object,
        source_ref: object,
    ) -> PoLine:
        packed = parse_po_line_row(
            purchase_order_id=purchase_order_id,
            line_code=line_code,
            sku_code=sku_code,
            qty=qty,
            uom_code=uom_code,
            plant_label=plant_label,
            batch_label=batch_label,
            serial_label=serial_label,
            coo_label=coo_label,
            source_ref=source_ref,
        )
        header = await self._rows.get_header(packed[0])
        if header is None:
            raise ResourceNotFound("nieznane zamówienie")
        return await self._rows.add_line(_line_row(organization_id, user_id, packed))


def _line_row(organization_id: UUID, user_id: UUID, packed: _PoLineParsed) -> PoLine:
    return PoLine(
        id=uuid4(),
        organization_id=organization_id,
        purchase_order_id=packed[0],
        line_code=packed[1],
        sku_code=packed[2],
        qty=packed[3],
        uom_code=packed[4],
        plant_label=packed[5],
        batch_label=packed[6],
        serial_label=packed[7],
        coo_label=packed[8],
        source_ref=packed[9],
        created_by=user_id,
    )
