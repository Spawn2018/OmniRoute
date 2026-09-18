from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.filing_bind_mark import FilingBindMark
from app.services.filing_bind_marks.filing_bind_mark_service import FilingBindMarkService

router = APIRouter(prefix="/filing-bind-marks", tags=["filing-bind-marks"])
_PERM = "can_manage_filing_bind_marks"


class FilingBindMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mark_code: str
    bind_kind: str
    source_ref: str


class FilingBindMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    mark_code: str
    bind_kind: str
    source_ref: str


def _row(saved: FilingBindMark) -> FilingBindMarkResponse:
    return FilingBindMarkResponse.model_validate(saved)


@router.get("", response_model=list[FilingBindMarkResponse])
async def list_filing_bind_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FilingBindMarkResponse]:
    return [_row(item) for item in await FilingBindMarkService(session).list_marks()]


@router.post("", response_model=FilingBindMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_filing_bind_mark(
    body: FilingBindMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FilingBindMarkResponse:
    saved = await FilingBindMarkService(session).persist_filing_bind_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bind_kind=body.bind_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
