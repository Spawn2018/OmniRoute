from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.local_charge_bind_mark import LocalChargeBindMark
from app.services.local_charge_bind_marks.local_charge_bind_mark_service import (
    LocalChargeBindMarkService,
)

router = APIRouter(
    prefix="/local-charge-bind-marks",
    tags=["local-charge-bind-marks"],
)

_PERM = "can_manage_local_charge_bind_marks"


class LocalChargeBindMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    bind_kind: str
    source_ref: str


class LocalChargeBindMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    bind_kind: str
    source_ref: str


def _as_response(row: LocalChargeBindMark) -> LocalChargeBindMarkResponse:
    return LocalChargeBindMarkResponse.model_validate(row)


@router.get("", response_model=list[LocalChargeBindMarkResponse])
async def list_local_charge_bind_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LocalChargeBindMarkResponse]:
    rows = await LocalChargeBindMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=LocalChargeBindMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_local_charge_bind_mark(
    body: LocalChargeBindMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LocalChargeBindMarkResponse:
    saved = await LocalChargeBindMarkService(session).persist_local_charge_bind_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bind_kind=body.bind_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
