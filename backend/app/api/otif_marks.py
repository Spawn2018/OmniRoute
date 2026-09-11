from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.otif_mark import OtifMark
from app.services.otif_marks.otif_mark_service import OtifMarkService

router = APIRouter(prefix="/otif-marks", tags=["otif-marks"])

_PERM = "can_manage_otif_marks"


class OtifMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    scope_kind: str
    source_ref: str


class OtifMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    scope_kind: str
    source_ref: str


def _mark(saved: OtifMark) -> OtifMarkResponse:
    return OtifMarkResponse.model_validate(saved)


@router.get("", response_model=list[OtifMarkResponse])
async def list_otif_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OtifMarkResponse]:
    packed = await OtifMarkService(session).list_marks()
    return [_mark(item) for item in packed]


@router.post(
    "",
    response_model=OtifMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_otif_mark(
    body: OtifMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OtifMarkResponse:
    saved = await OtifMarkService(session).persist_otif_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        scope_kind=body.scope_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _mark(saved)
