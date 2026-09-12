"""HTTP katalog A/B+SUS — HITL, bez live mapa/GPS."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ab_sus_mark import AbSusMark
from app.services.ab_sus_marks.ab_sus_mark_service import AbSusMarkService

router = APIRouter(prefix="/ab-sus-marks", tags=["ab-sus"])

_PERM = "can_manage_ab_sus_marks"

class AbSusMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    trial_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)

class AbSusMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    trial_kind: str
    source_ref: str

def _to_dto(row: AbSusMark) -> AbSusMarkResponse:
    return AbSusMarkResponse.model_validate(row)

@router.get("", response_model=list[AbSusMarkResponse])
async def list_ab_sus_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AbSusMarkResponse]:
    catalog = AbSusMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]

@router.post("", response_model=AbSusMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_ab_sus_mark(
    body: AbSusMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AbSusMarkResponse:
    catalog = AbSusMarkService(session)
    saved = await catalog.persist_ab_sus_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        trial_kind=body.trial_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "ab-sus-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
