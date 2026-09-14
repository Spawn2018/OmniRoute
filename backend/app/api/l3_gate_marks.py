from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.l3_gate_mark import L3GateMark
from app.services.l3_gate_marks.l3_gate_mark_service import L3GateMarkService

router = APIRouter(
    prefix="/l3-gate-marks",
    tags=["l3-gate-marks"],
)

_PERM = "can_manage_l3_gate_marks"


class L3GateMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    gate_kind: str
    source_ref: str


class L3GateMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    gate_kind: str
    source_ref: str


def _row(saved: L3GateMark) -> L3GateMarkResponse:
    return L3GateMarkResponse.model_validate(saved)


@router.get("", response_model=list[L3GateMarkResponse])
async def list_l3_gate_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[L3GateMarkResponse]:
    packed = await L3GateMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=L3GateMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_l3_gate_mark(
    body: L3GateMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> L3GateMarkResponse:
    saved = await L3GateMarkService(session).persist_l3_gate_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        gate_kind=body.gate_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
