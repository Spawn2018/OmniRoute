from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipper_award_mark import ShipperAwardMark
from app.services.shipper_award_marks.shipper_award_mark_service import ShipperAwardMarkService

router = APIRouter(prefix="/shipper-award-marks", tags=["shipper-award-marks"])


class ShipperAwardMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(description="snake HITL")
    award_kind: str = Field(description="go|hold|no_award|other")
    source_ref: str = Field(description="tenant:manual lub fixture")


class ShipperAwardMarkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    award_kind: str
    source_ref: str


@router.get("", response_model=list[ShipperAwardMarkOut])
async def list_shipper_award_marks(
    _authz: None = Depends(
        require_permission("can_manage_shipper_award_marks", "organization"),
    ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipperAwardMarkOut]:
    service = ShipperAwardMarkService(session)
    return [ShipperAwardMarkOut.model_validate(row) for row in await service.list_marks()]


@router.post("", response_model=ShipperAwardMarkOut, status_code=status.HTTP_201_CREATED)
async def create_shipper_award_mark(
    body: ShipperAwardMarkCreate,
    _authz: None = Depends(
        require_permission("can_manage_shipper_award_marks", "organization"),
    ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipperAwardMarkOut:
    service = ShipperAwardMarkService(session)
    saved: ShipperAwardMark = await service.persist_shipper_award_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        award_kind=body.award_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return ShipperAwardMarkOut.model_validate(saved)
