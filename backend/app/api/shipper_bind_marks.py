from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipper_bind_mark import ShipperBindMark
from app.services.shipper_bind_marks.shipper_bind_mark_service import ShipperBindMarkService

router = APIRouter(prefix="/shipper-bind-marks", tags=["shipper-bind-marks"])

_REL = "can_manage_shipper_bind_marks"


class ShipperBindMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    bind_kind: str
    source_ref: str


class ShipperBindMarkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    bind_kind: str
    source_ref: str


def _out(row: ShipperBindMark) -> ShipperBindMarkOut:
    return ShipperBindMarkOut.model_validate(row)


@router.get("", response_model=list[ShipperBindMarkOut])
async def list_shipper_bind_marks(
    _authz: None = Depends(require_permission(_REL, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipperBindMarkOut]:
    found = await ShipperBindMarkService(session).list_marks()
    return [_out(item) for item in found]


@router.post("", response_model=ShipperBindMarkOut, status_code=status.HTTP_201_CREATED)
async def create_shipper_bind_mark(
    body: ShipperBindMarkCreate,
    _authz: None = Depends(require_permission(_REL, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipperBindMarkOut:
    saved = await ShipperBindMarkService(session).persist_shipper_bind_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bind_kind=body.bind_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _out(saved)
