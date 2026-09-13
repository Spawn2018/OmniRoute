from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.telematics_device import TelematicsDevice
from app.services.telematics_devices.telematics_device_service import (
    TelematicsDeviceService,
)

router = APIRouter(prefix="/telematics-devices", tags=["telematics-devices"])

_PERM = "can_manage_telematics_devices"


class TelematicsDeviceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    device_code: str
    device_kind: str
    source_ref: str


class TelematicsDeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    device_code: str
    device_kind: str
    source_ref: str


def _row(saved: TelematicsDevice) -> TelematicsDeviceResponse:
    return TelematicsDeviceResponse.model_validate(saved)


@router.get("", response_model=list[TelematicsDeviceResponse])
async def list_telematics_devices(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TelematicsDeviceResponse]:
    packed = await TelematicsDeviceService(session).list_devices()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=TelematicsDeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_telematics_device(
    body: TelematicsDeviceCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TelematicsDeviceResponse:
    saved = await TelematicsDeviceService(session).persist_telematics_device(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        device_code=body.device_code,
        device_kind=body.device_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
