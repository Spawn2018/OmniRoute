from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.oog_mark import OogMark
from app.services.oog_marks.oog_mark_service import OogMarkService

router = APIRouter(prefix="/oog-marks", tags=["oog-marks"])

_PERM = "can_manage_oog_marks"


class OogMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    escort_kind: str
    source_ref: str


class OogMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    escort_kind: str
    source_ref: str


def _row(saved: OogMark) -> OogMarkResponse:
    return OogMarkResponse.model_validate(saved)


@router.get("", response_model=list[OogMarkResponse])
async def list_oog_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OogMarkResponse]:
    packed = await OogMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=OogMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_oog_mark(
    body: OogMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OogMarkResponse:
    saved = await OogMarkService(session).persist_oog_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        escort_kind=body.escort_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
