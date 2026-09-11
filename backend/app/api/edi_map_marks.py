from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.edi_map_mark import EdiMapMark
from app.services.edi_map_marks.edi_map_mark_service import EdiMapMarkService

router = APIRouter(prefix="/edi-map-marks", tags=["edi-map-marks"])

_PERM = "can_manage_edi_map_marks"


class EdiMapMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    map_kind: str
    source_ref: str


class EdiMapMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    map_kind: str
    source_ref: str


def _row(saved: EdiMapMark) -> EdiMapMarkResponse:
    return EdiMapMarkResponse.model_validate(saved)


@router.get("", response_model=list[EdiMapMarkResponse])
async def list_edi_map_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[EdiMapMarkResponse]:
    packed = await EdiMapMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=EdiMapMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_edi_map_mark(
    body: EdiMapMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> EdiMapMarkResponse:
    saved = await EdiMapMarkService(session).persist_edi_map_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        map_kind=body.map_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
