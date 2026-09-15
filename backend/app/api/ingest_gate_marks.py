from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ingest_gate_mark import IngestGateMark
from app.services.ingest_gate_marks.ingest_gate_mark_service import (
    IngestGateMarkService,
)

router = APIRouter(
    prefix="/ingest-gate-marks",
    tags=["ingest-gate-marks"],
)

_PERM = "can_manage_ingest_gate_marks"


class IngestGateMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    gate_kind: str
    source_ref: str


class IngestGateMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    gate_kind: str
    source_ref: str


def _row(saved: IngestGateMark) -> IngestGateMarkResponse:
    return IngestGateMarkResponse.model_validate(saved)


@router.get("", response_model=list[IngestGateMarkResponse])
async def list_ingest_gate_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[IngestGateMarkResponse]:
    packed = await IngestGateMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=IngestGateMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ingest_gate_mark(
    body: IngestGateMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> IngestGateMarkResponse:
    saved = await IngestGateMarkService(session).persist_ingest_gate_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        gate_kind=body.gate_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
