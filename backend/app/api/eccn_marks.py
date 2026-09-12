from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.eccn_mark import EccnMark
from app.services.eccn_marks.eccn_mark_service import (
    EccnMarkService,
)

router = APIRouter(prefix="/eccn-marks", tags=["eccn-marks"])

_PERM = "can_manage_eccn_marks"


class EccnMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    control_kind: str
    source_ref: str


class EccnMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    control_kind: str
    source_ref: str


def _row(saved: EccnMark) -> EccnMarkResponse:
    return EccnMarkResponse.model_validate(saved)


@router.get("", response_model=list[EccnMarkResponse])
async def list_eccn_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[EccnMarkResponse]:
    packed = await EccnMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=EccnMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_eccn_mark(
    body: EccnMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> EccnMarkResponse:
    saved = await EccnMarkService(session).persist_eccn_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        control_kind=body.control_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
