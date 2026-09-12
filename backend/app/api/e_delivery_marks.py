from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.e_delivery_mark import EDeliveryMark
from app.services.e_delivery_marks.e_delivery_mark_service import (
    EDeliveryMarkService,
)

router = APIRouter(prefix="/e-delivery-marks", tags=["e-delivery-marks"])

_PERM = "can_manage_e_delivery_marks"


class EDeliveryMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    delivery_kind: str
    source_ref: str


class EDeliveryMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    delivery_kind: str
    source_ref: str


def _row(saved: EDeliveryMark) -> EDeliveryMarkResponse:
    return EDeliveryMarkResponse.model_validate(saved)


@router.get("", response_model=list[EDeliveryMarkResponse])
async def list_e_delivery_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[EDeliveryMarkResponse]:
    packed = await EDeliveryMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=EDeliveryMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_e_delivery_mark(
    body: EDeliveryMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> EDeliveryMarkResponse:
    saved = await EDeliveryMarkService(session).persist_e_delivery_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        delivery_kind=body.delivery_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
