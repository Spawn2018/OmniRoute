from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.fuel_anomaly_mark import FuelAnomalyMark
from app.services.fuel_anomaly_marks.fuel_anomaly_mark_service import (
    FuelAnomalyMarkService,
)

router = APIRouter(prefix="/fuel-anomaly-marks", tags=["fuel-anomaly-marks"])

_PERM = "can_manage_fuel_anomaly_marks"


class FuelAnomalyMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    anomaly_kind: str
    source_ref: str


class FuelAnomalyMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    anomaly_kind: str
    source_ref: str


def _row(saved: FuelAnomalyMark) -> FuelAnomalyMarkResponse:
    return FuelAnomalyMarkResponse.model_validate(saved)


@router.get("", response_model=list[FuelAnomalyMarkResponse])
async def list_fuel_anomaly_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FuelAnomalyMarkResponse]:
    packed = await FuelAnomalyMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=FuelAnomalyMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_fuel_anomaly_mark(
    body: FuelAnomalyMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FuelAnomalyMarkResponse:
    saved = await FuelAnomalyMarkService(session).persist_fuel_anomaly_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        anomaly_kind=body.anomaly_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
