from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import NetworkPrintGateMarkConflict
from app.domain.network_print_gate_mark import parse_network_print_gate_mark_row
from app.models.network_print_gate_mark import NetworkPrintGateMark
from app.repositories.network_print_gate_marks.network_print_gate_mark_repository import (
    NetworkPrintGateMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_network_print_gate_mark_org_code" in detail:
        raise NetworkPrintGateMarkConflict(
            "ten kod bramy wydruku sieci już istnieje",
        ) from orig
    if "uq_network_print_gate_mark_org_source_ref" in detail:
        raise NetworkPrintGateMarkConflict(
            "to wskazanie bramy wydruku sieci już istnieje",
        ) from orig
    raise orig


class NetworkPrintGateMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = NetworkPrintGateMarkRepository(session)

    async def list_marks(self) -> list[NetworkPrintGateMark]:
        return await self._repo.list_marks()

    async def persist_network_print_gate_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        gate_kind: object,
        source_ref: object,
    ) -> NetworkPrintGateMark:
        code, kind, origin = parse_network_print_gate_mark_row(
            mark_code,
            gate_kind,
            source_ref,
        )
        row = NetworkPrintGateMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            gate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._repo.add_mark(row)
        except IntegrityError as exc:
            _raise_create_conflict(exc)
