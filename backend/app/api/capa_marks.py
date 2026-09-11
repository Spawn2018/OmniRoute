from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.capa_mark import CapaMark
from app.services.capa_marks.capa_mark_service import CapaMarkService

router = APIRouter(prefix="/capa-marks", tags=["capa-marks"])

_PERM = "can_manage_capa_marks"


class CapaMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    mark_kind: str
    source_ref: str


class CapaMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    mark_kind: str
    source_ref: str


def _mark(saved: CapaMark) -> CapaMarkResponse:
    return CapaMarkResponse.model_validate(saved)


@router.get("", response_model=list[CapaMarkResponse])
async def list_capa_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CapaMarkResponse]:
    packed = await CapaMarkService(session).list_marks()
    return [_mark(item) for item in packed]


@router.post(
    "",
    response_model=CapaMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_capa_mark(
    body: CapaMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CapaMarkResponse:
    saved = await CapaMarkService(session).persist_capa_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        mark_kind=body.mark_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _mark(saved)
