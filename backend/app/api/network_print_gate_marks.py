from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.network_print_gate_mark import NetworkPrintGateMark
from app.services.network_print_gate_marks.network_print_gate_mark_service import (
    NetworkPrintGateMarkService,
)

router = APIRouter(
    prefix="/network-print-gate-marks",
    tags=["network-print-gate-marks"],
)

_PERM = "can_manage_network_print_gate_marks"


class NetworkPrintGateMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    gate_kind: str
    source_ref: str


class NetworkPrintGateMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    gate_kind: str
    source_ref: str


def _as_response(row: NetworkPrintGateMark) -> NetworkPrintGateMarkResponse:
    return NetworkPrintGateMarkResponse.model_validate(row)


@router.get("", response_model=list[NetworkPrintGateMarkResponse])
async def list_network_print_gate_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NetworkPrintGateMarkResponse]:
    rows = await NetworkPrintGateMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=NetworkPrintGateMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_network_print_gate_mark(
    body: NetworkPrintGateMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NetworkPrintGateMarkResponse:
    saved = await NetworkPrintGateMarkService(session).persist_network_print_gate_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        gate_kind=body.gate_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
