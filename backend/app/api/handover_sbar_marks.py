from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.handover_sbar_mark import HandoverSbarMark
from app.services.handover_sbar_marks.handover_sbar_mark_service import (
    HandoverSbarMarkService,
)

router = APIRouter(
    prefix="/handover-sbar-marks",
    tags=["handover-sbar-marks"],
)

_PERM = "can_manage_handover_sbar_marks"


class HandoverSbarMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    sbar_kind: str
    source_ref: str


class HandoverSbarMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    sbar_kind: str
    source_ref: str


def _row(saved: HandoverSbarMark) -> HandoverSbarMarkResponse:
    return HandoverSbarMarkResponse.model_validate(saved)


@router.get("", response_model=list[HandoverSbarMarkResponse])
async def list_handover_sbar_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[HandoverSbarMarkResponse]:
    packed = await HandoverSbarMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=HandoverSbarMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_handover_sbar_mark(
    body: HandoverSbarMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> HandoverSbarMarkResponse:
    saved = await HandoverSbarMarkService(session).persist_handover_sbar_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        sbar_kind=body.sbar_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
