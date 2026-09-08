from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.incoterm_responsibility import (
    omni_ops_seed_pairs,
    require_booking_scope,
    require_clearance_role,
    require_main_carriage_booker,
    require_responsibility_incoterm,
    require_responsibility_source_ref,
    require_responsibility_trade_side,
)
from app.models.incoterm_responsibility import IncotermResponsibility
from app.repositories.incoterm_responsibilities.incoterm_responsibility_repository import (
    IncotermResponsibilityRepository,
)


class IncotermResponsibilityService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = IncotermResponsibilityRepository(session)

    async def list_for_pair(
        self,
        *,
        incoterm: object,
        trade_side: object,
    ) -> list[IncotermResponsibility]:
        return await self._rows.list_current_for_pair(
            require_responsibility_incoterm(incoterm),
            require_responsibility_trade_side(trade_side),
        )

    async def record_rule(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incoterm: object,
        trade_side: object,
        export_clearance_role: object,
        import_clearance_role: object,
        main_carriage_booker: object,
        booking_scope: object,
        source_ref: object,
    ) -> IncotermResponsibility:
        code = require_responsibility_incoterm(incoterm)
        side = require_responsibility_trade_side(trade_side)
        payload = (
            require_clearance_role(export_clearance_role, field="export_clearance_role"),
            require_clearance_role(import_clearance_role, field="import_clearance_role"),
            require_main_carriage_booker(main_carriage_booker),
            require_booking_scope(booking_scope),
            require_responsibility_source_ref(source_ref),
        )
        current = await self._rows.find_current(code, side)
        if current is not None and _same_payload(current, payload):
            return current
        saved = await self._rows.add(
            _new_row(organization_id, user_id, code, side, payload),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved

    async def seed_omni_ops(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
    ) -> list[IncotermResponsibility]:
        present = {
            (str(row.incoterm).strip(), row.trade_side)
            for row in await self._rows.list_current()
        }
        for pair in omni_ops_seed_pairs():
            key = (str(pair["incoterm"]), str(pair["trade_side"]))
            if key in present:
                continue
            await self.record_rule(
                organization_id=organization_id,
                user_id=user_id,
                incoterm=pair["incoterm"],
                trade_side=pair["trade_side"],
                export_clearance_role=pair["export_clearance_role"],
                import_clearance_role=pair["import_clearance_role"],
                main_carriage_booker=pair["main_carriage_booker"],
                booking_scope=pair["booking_scope"],
                source_ref=pair["source_ref"],
            )
            present.add(key)
        return await self._rows.list_current()


def _new_row(
    organization_id: UUID,
    user_id: UUID,
    code: str,
    side: str,
    payload: tuple[str, str, str, list[str], str],
) -> IncotermResponsibility:
    return IncotermResponsibility(
        id=uuid4(),
        organization_id=organization_id,
        incoterm=code,
        trade_side=side,
        export_clearance_role=payload[0],
        import_clearance_role=payload[1],
        main_carriage_booker=payload[2],
        booking_scope=payload[3],
        source_ref=payload[4],
        created_by=user_id,
    )


def _same_payload(
    row: IncotermResponsibility,
    payload: tuple[str, str, str, list[str], str],
) -> bool:
    return (
        row.export_clearance_role == payload[0]
        and row.import_clearance_role == payload[1]
        and row.main_carriage_booker == payload[2]
        and list(row.booking_scope) == payload[3]
        and row.source_ref == payload[4]
    )
