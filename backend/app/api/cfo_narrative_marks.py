from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cfo_narrative_mark import CfoNarrativeMark
from app.services.cfo_narrative_marks.cfo_narrative_mark_service import (
    CfoNarrativeMarkService,
)

router = APIRouter(
    prefix="/cfo-narrative-marks",
    tags=["cfo-narrative-marks"],
)

_PERM = "can_manage_cfo_narrative_marks"


class CfoNarrativeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    narrative_kind: str
    source_ref: str


class CfoNarrativeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    narrative_kind: str
    source_ref: str


def _row(saved: CfoNarrativeMark) -> CfoNarrativeMarkResponse:
    return CfoNarrativeMarkResponse.model_validate(saved)


@router.get("", response_model=list[CfoNarrativeMarkResponse])
async def list_cfo_narrative_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CfoNarrativeMarkResponse]:
    packed = await CfoNarrativeMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CfoNarrativeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cfo_narrative_mark(
    body: CfoNarrativeMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CfoNarrativeMarkResponse:
    saved = await CfoNarrativeMarkService(session).persist_cfo_narrative_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        narrative_kind=body.narrative_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
