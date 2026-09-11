from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cabotage_mark import CabotageMark
from app.services.cabotage_marks.cabotage_mark_service import (
    CabotageMarkService,
)

router = APIRouter(prefix="/cabotage-marks", tags=["cabotage-marks"])

_PERM = "can_manage_cabotage_marks"


class CabotageMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    cabotage_kind: str
    source_ref: str


class CabotageMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    cabotage_kind: str
    source_ref: str


def _row(saved: CabotageMark) -> CabotageMarkResponse:
    return CabotageMarkResponse.model_validate(saved)


@router.get("", response_model=list[CabotageMarkResponse])
async def list_cabotage_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CabotageMarkResponse]:
    packed = await CabotageMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CabotageMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cabotage_mark(
    body: CabotageMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CabotageMarkResponse:
    saved = await CabotageMarkService(session).persist_cabotage_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        cabotage_kind=body.cabotage_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
