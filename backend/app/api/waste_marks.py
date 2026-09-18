from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.waste_mark import WasteMark
from app.services.waste_marks.waste_mark_service import WasteMarkService

router = APIRouter(prefix="/waste-marks", tags=["waste-marks"])

_PERM = "can_manage_waste_marks"


class WasteMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    waste_kind: str
    source_ref: str


class WasteMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    waste_kind: str
    source_ref: str


def _row(saved: WasteMark) -> WasteMarkResponse:
    return WasteMarkResponse.model_validate(saved)


@router.get("", response_model=list[WasteMarkResponse])
async def list_waste_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[WasteMarkResponse]:
    packed = await WasteMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post("", response_model=WasteMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_waste_mark(
    body: WasteMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> WasteMarkResponse:
    saved = await WasteMarkService(session).persist_waste_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        waste_kind=body.waste_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
