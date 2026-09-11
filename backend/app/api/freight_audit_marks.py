from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.freight_audit_mark import FreightAuditMark
from app.services.freight_audit_marks.freight_audit_mark_service import (
    FreightAuditMarkService,
)

router = APIRouter(prefix="/freight-audit-marks", tags=["freight-audit-marks"])

_PERM = "can_manage_freight_audit_marks"


class FreightAuditMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    audit_kind: str
    source_ref: str


class FreightAuditMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    audit_kind: str
    source_ref: str


def _mark(saved: FreightAuditMark) -> FreightAuditMarkResponse:
    return FreightAuditMarkResponse.model_validate(saved)


@router.get("", response_model=list[FreightAuditMarkResponse])
async def list_freight_audit_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FreightAuditMarkResponse]:
    packed = await FreightAuditMarkService(session).list_marks()
    return [_mark(item) for item in packed]


@router.post(
    "",
    response_model=FreightAuditMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_freight_audit_mark(
    body: FreightAuditMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FreightAuditMarkResponse:
    saved = await FreightAuditMarkService(session).persist_freight_audit_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        audit_kind=body.audit_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _mark(saved)
