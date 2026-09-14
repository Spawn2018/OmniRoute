from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.risk_register_mark import RiskRegisterMark
from app.services.risk_register_marks.risk_register_mark_service import (
    RiskRegisterMarkService,
)

router = APIRouter(
    prefix="/risk-register-marks",
    tags=["risk-register-marks"],
)

_PERM = "can_manage_risk_register_marks"


class RiskRegisterMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    risk_kind: str
    source_ref: str


class RiskRegisterMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    risk_kind: str
    source_ref: str


def _row(saved: RiskRegisterMark) -> RiskRegisterMarkResponse:
    return RiskRegisterMarkResponse.model_validate(saved)


@router.get("", response_model=list[RiskRegisterMarkResponse])
async def list_risk_register_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RiskRegisterMarkResponse]:
    packed = await RiskRegisterMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=RiskRegisterMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_risk_register_mark(
    body: RiskRegisterMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RiskRegisterMarkResponse:
    saved = await RiskRegisterMarkService(session).persist_risk_register_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        risk_kind=body.risk_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
