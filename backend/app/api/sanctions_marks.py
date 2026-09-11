from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.sanctions_mark import SanctionsMark
from app.services.sanctions_marks.sanctions_mark_service import (
    SanctionsMarkService,
)

router = APIRouter(prefix="/sanctions-marks", tags=["sanctions-marks"])

_PERM = "can_manage_sanctions_marks"


class SanctionsMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    list_kind: str
    source_ref: str


class SanctionsMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    list_kind: str
    source_ref: str


def _row(saved: SanctionsMark) -> SanctionsMarkResponse:
    return SanctionsMarkResponse.model_validate(saved)


@router.get("", response_model=list[SanctionsMarkResponse])
async def list_sanctions_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SanctionsMarkResponse]:
    packed = await SanctionsMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=SanctionsMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sanctions_mark(
    body: SanctionsMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SanctionsMarkResponse:
    saved = await SanctionsMarkService(session).persist_sanctions_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        list_kind=body.list_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
