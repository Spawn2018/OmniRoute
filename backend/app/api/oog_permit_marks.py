from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.oog_permit_mark import OogPermitMark
from app.services.oog_permit_marks.oog_permit_mark_service import OogPermitMarkService

router = APIRouter(prefix="/oog-permit-marks", tags=["oog-permit-marks"])

_PERM = "can_manage_oog_permit_marks"


class OogPermitMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    permit_kind: str
    source_ref: str


class OogPermitMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    permit_kind: str
    source_ref: str


def _row(saved: OogPermitMark) -> OogPermitMarkResponse:
    return OogPermitMarkResponse.model_validate(saved)


@router.get("", response_model=list[OogPermitMarkResponse])
async def list_oog_permit_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OogPermitMarkResponse]:
    packed = await OogPermitMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=OogPermitMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_oog_permit_mark(
    body: OogPermitMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OogPermitMarkResponse:
    saved = await OogPermitMarkService(session).persist_oog_permit_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        permit_kind=body.permit_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
