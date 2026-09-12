from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.peppol_mark import PeppolMark
from app.services.peppol_marks.peppol_mark_service import (
    PeppolMarkService,
)

router = APIRouter(prefix="/peppol-marks", tags=["peppol-marks"])

_PERM = "can_manage_peppol_marks"


class PeppolMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    peppol_kind: str
    source_ref: str


class PeppolMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    peppol_kind: str
    source_ref: str


def _row(saved: PeppolMark) -> PeppolMarkResponse:
    return PeppolMarkResponse.model_validate(saved)


@router.get("", response_model=list[PeppolMarkResponse])
async def list_peppol_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PeppolMarkResponse]:
    packed = await PeppolMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PeppolMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_peppol_mark(
    body: PeppolMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PeppolMarkResponse:
    saved = await PeppolMarkService(session).persist_peppol_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        peppol_kind=body.peppol_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
