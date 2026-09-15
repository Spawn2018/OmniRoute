from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.compliance_program_mark import ComplianceProgramMark
from app.services.compliance_program_marks.compliance_program_mark_service import (
    ComplianceProgramMarkService,
)

router = APIRouter(
    prefix="/compliance-program-marks",
    tags=["compliance-program-marks"],
)

_PERM = "can_manage_compliance_program_marks"


class ComplianceProgramMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    program_kind: str
    source_ref: str


class ComplianceProgramMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    program_kind: str
    source_ref: str


def _row(saved: ComplianceProgramMark) -> ComplianceProgramMarkResponse:
    return ComplianceProgramMarkResponse.model_validate(saved)


@router.get("", response_model=list[ComplianceProgramMarkResponse])
async def list_compliance_program_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ComplianceProgramMarkResponse]:
    packed = await ComplianceProgramMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ComplianceProgramMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_compliance_program_mark(
    body: ComplianceProgramMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ComplianceProgramMarkResponse:
    saved = await ComplianceProgramMarkService(session).persist_compliance_program_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        program_kind=body.program_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
