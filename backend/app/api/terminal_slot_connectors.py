from datetime import time
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.terminal_slot_connector import TerminalSlotConnector
from app.services.terminal_slot_connectors.terminal_slot_connector_service import (
    TerminalSlotConnectorService,
)

router = APIRouter(prefix="/terminal-slot-connectors", tags=["terminal-slot-connectors"])

_PERM = "can_manage_terminal_slot_connectors"


class TerminalSlotConnectorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connector_code: str
    terminal_code: str
    mode: str
    opens_local: str
    closes_local: str
    cutoff_local: str
    source_ref: str


class TerminalSlotConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connector_code: str
    terminal_code: str
    mode: str
    opens_local: time
    closes_local: time
    cutoff_local: time
    source_ref: str


def _as_row(row: TerminalSlotConnector) -> TerminalSlotConnectorResponse:
    return TerminalSlotConnectorResponse(
        id=row.id,
        organization_id=row.organization_id,
        connector_code=row.connector_code,
        terminal_code=row.terminal_code,
        mode=row.mode,
        opens_local=row.opens_local,
        closes_local=row.closes_local,
        cutoff_local=row.cutoff_local,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TerminalSlotConnectorResponse])
async def list_terminal_slot_connectors(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TerminalSlotConnectorResponse]:
    rows = await TerminalSlotConnectorService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TerminalSlotConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_terminal_slot_connector(
    body: TerminalSlotConnectorCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TerminalSlotConnectorResponse:
    row = await TerminalSlotConnectorService(session).persist_terminal_slot_connector(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        connector_code=body.connector_code,
        terminal_code=body.terminal_code,
        mode=body.mode,
        opens_local=body.opens_local,
        closes_local=body.closes_local,
        cutoff_local=body.cutoff_local,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
