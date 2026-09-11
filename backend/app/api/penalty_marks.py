from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.penalty_mark import PenaltyMark
from app.services.penalty_marks.penalty_mark_service import PenaltyMarkService

router = APIRouter(prefix="/penalty-marks", tags=["penalty-marks"])

_PERM = "can_manage_penalty_marks"


class PenaltyMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    breach_kind: str
    source_ref: str


class PenaltyMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    breach_kind: str
    source_ref: str


def _mark(saved: PenaltyMark) -> PenaltyMarkResponse:
    return PenaltyMarkResponse.model_validate(saved)


@router.get("", response_model=list[PenaltyMarkResponse])
async def list_penalty_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PenaltyMarkResponse]:
    packed = await PenaltyMarkService(session).list_marks()
    return [_mark(item) for item in packed]


@router.post(
    "",
    response_model=PenaltyMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_penalty_mark(
    body: PenaltyMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PenaltyMarkResponse:
    saved = await PenaltyMarkService(session).persist_penalty_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        breach_kind=body.breach_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _mark(saved)
