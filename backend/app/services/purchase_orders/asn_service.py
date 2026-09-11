from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.asn import parse_asn_row
from app.domain.errors import ResourceNotFound
from app.models.asn import Asn
from app.repositories.purchase_orders.asn_repository import AsnRepository

_AsnParsed = tuple[UUID, str, str | None, str | None, str | None, str | None, str]


class AsnService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = AsnRepository(session)

    async def list_notices(self) -> list[Asn]:
        return await self._rows.list_notices()

    async def persist_asn(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        purchase_order_id: object,
        asn_code: object,
        plant_label: object,
        carrier_label: object,
        ship_ref_label: object,
        guide_code: object,
        source_ref: object,
    ) -> Asn:
        packed = parse_asn_row(
            purchase_order_id=purchase_order_id,
            asn_code=asn_code,
            plant_label=plant_label,
            carrier_label=carrier_label,
            ship_ref_label=ship_ref_label,
            guide_code=guide_code,
            source_ref=source_ref,
        )
        header = await self._rows.get_header(packed[0])
        if header is None:
            raise ResourceNotFound("nieznane zamówienie")
        return await self._rows.add_notice(_notice_row(organization_id, user_id, packed))


def _notice_row(organization_id: UUID, user_id: UUID, packed: _AsnParsed) -> Asn:
    return Asn(
        id=uuid4(),
        organization_id=organization_id,
        purchase_order_id=packed[0],
        asn_code=packed[1],
        plant_label=packed[2],
        carrier_label=packed[3],
        ship_ref_label=packed[4],
        guide_code=packed[5],
        source_ref=packed[6],
        created_by=user_id,
    )
