from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.switch_bl_loi_mark import SwitchBlLoiMark
from app.services.switch_bl_loi_marks.switch_bl_loi_mark_service import (
    SwitchBlLoiMarkService,
)

router = APIRouter(prefix="/switch-bl-loi-marks", tags=["switch-bl-loi-marks"])

_PERM = "can_manage_switch_bl_loi_marks"


class SwitchBlLoiMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    instrument_kind: str
    source_ref: str


class SwitchBlLoiMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    instrument_kind: str
    source_ref: str


def _row(saved: SwitchBlLoiMark) -> SwitchBlLoiMarkResponse:
    return SwitchBlLoiMarkResponse.model_validate(saved)


@router.get("", response_model=list[SwitchBlLoiMarkResponse])
async def list_switch_bl_loi_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SwitchBlLoiMarkResponse]:
    packed = await SwitchBlLoiMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=SwitchBlLoiMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_switch_bl_loi_mark(
    body: SwitchBlLoiMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SwitchBlLoiMarkResponse:
    saved = await SwitchBlLoiMarkService(session).persist_switch_bl_loi_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        instrument_kind=body.instrument_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
