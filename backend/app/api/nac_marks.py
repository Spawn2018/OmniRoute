from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.nac_mark import NacMark
from app.services.nac_marks.nac_mark_service import NacMarkService

router = APIRouter(prefix="/nac-marks", tags=["nac-marks"])

_PERM = "can_manage_nac_marks"


class NacMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    nac_kind: str
    source_ref: str


class NacMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    nac_kind: str
    source_ref: str


def _row(saved: NacMark) -> NacMarkResponse:
    return NacMarkResponse.model_validate(saved)


@router.get("", response_model=list[NacMarkResponse])
async def list_nac_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NacMarkResponse]:
    packed = await NacMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=NacMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_nac_mark(
    body: NacMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NacMarkResponse:
    saved = await NacMarkService(session).persist_nac_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        nac_kind=body.nac_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
