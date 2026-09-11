from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.combined_transport_mark import CombinedTransportMark
from app.services.combined_transport_marks.combined_transport_mark_service import (
    CombinedTransportMarkService,
)

router = APIRouter(prefix="/combined-transport-marks", tags=["combined-transport-marks"])

_PERM = "can_manage_combined_transport_marks"


class CombinedTransportMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    regime_kind: str
    source_ref: str


class CombinedTransportMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    regime_kind: str
    source_ref: str


def _row(saved: CombinedTransportMark) -> CombinedTransportMarkResponse:
    return CombinedTransportMarkResponse.model_validate(saved)


@router.get("", response_model=list[CombinedTransportMarkResponse])
async def list_combined_transport_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CombinedTransportMarkResponse]:
    packed = await CombinedTransportMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CombinedTransportMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_combined_transport_mark(
    body: CombinedTransportMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CombinedTransportMarkResponse:
    saved = await CombinedTransportMarkService(session).persist_combined_transport_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        regime_kind=body.regime_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
