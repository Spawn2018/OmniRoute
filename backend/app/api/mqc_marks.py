from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.mqc_mark import MqcMark
from app.services.mqc_marks.mqc_mark_service import (
    MqcMarkService,
)

router = APIRouter(prefix="/mqc-marks", tags=["mqc-marks"])

_PERM = "can_manage_mqc_marks"


class MqcMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    mqc_kind: str
    source_ref: str


class MqcMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    mqc_kind: str
    source_ref: str


def _row(saved: MqcMark) -> MqcMarkResponse:
    return MqcMarkResponse.model_validate(saved)


@router.get("", response_model=list[MqcMarkResponse])
async def list_mqc_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MqcMarkResponse]:
    packed = await MqcMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=MqcMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_mqc_mark(
    body: MqcMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MqcMarkResponse:
    saved = await MqcMarkService(session).persist_mqc_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        mqc_kind=body.mqc_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
