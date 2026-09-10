from datetime import time
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.terminal_slot_connector import (
    require_connector_code,
    require_cutoff_clock,
    require_gate_clock,
    require_slot_mode,
    require_slot_source_ref,
    require_terminal_code,
)
from app.models.terminal_slot_connector import TerminalSlotConnector
from app.repositories.terminal_slot_connectors.terminal_slot_connector_repository import (
    TerminalSlotConnectorRepository,
)


class TerminalSlotConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TerminalSlotConnectorRepository(session)

    async def list_rows(self) -> list[TerminalSlotConnector]:
        return await self._rows.fetch_rows()

    async def persist_terminal_slot_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        terminal_code: object,
        mode: object,
        opens_local: object,
        closes_local: object,
        cutoff_local: object,
        source_ref: object,
    ) -> TerminalSlotConnector:
        opens: time = require_gate_clock(opens_local)
        closes: time = require_gate_clock(closes_local)
        cutoff: time = require_cutoff_clock(cutoff_local)
        row = TerminalSlotConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            terminal_code=require_terminal_code(terminal_code),
            mode=require_slot_mode(mode),
            opens_local=opens,
            closes_local=closes,
            cutoff_local=cutoff,
            source_ref=require_slot_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
