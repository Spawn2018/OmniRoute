from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.local_charge_warning_mark import LocalChargeWarningMark
from app.services.local_charge_warning_marks.local_charge_warning_mark_service import (
    LocalChargeWarningMarkService,
)

router = APIRouter(
    prefix="/local-charge-warning-marks",
    tags=["local-charge-warning-marks"],
)

_PERM = "can_manage_local_charge_warning_marks"


class LocalChargeWarningMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    warning_kind: str
    source_ref: str


class LocalChargeWarningMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    warning_kind: str
    source_ref: str


def _as_response(row: LocalChargeWarningMark) -> LocalChargeWarningMarkResponse:
    return LocalChargeWarningMarkResponse.model_validate(row)


@router.get("", response_model=list[LocalChargeWarningMarkResponse])
async def list_local_charge_warning_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LocalChargeWarningMarkResponse]:
    rows = await LocalChargeWarningMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=LocalChargeWarningMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_local_charge_warning_mark(
    body: LocalChargeWarningMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LocalChargeWarningMarkResponse:
    saved = await LocalChargeWarningMarkService(session).persist_local_charge_warning_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        warning_kind=body.warning_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
