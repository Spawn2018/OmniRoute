from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.filing_fk_mark import FilingFkMark
from app.services.filing_fk_marks.filing_fk_mark_service import FilingFkMarkService

router = APIRouter(
    prefix="/filing-fk-marks",
    tags=["filing-fk-marks"],
)

_PERM = "can_manage_filing_fk_marks"


class FilingFkMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    fk_kind: str
    source_ref: str


class FilingFkMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    fk_kind: str
    source_ref: str


def _row(saved: FilingFkMark) -> FilingFkMarkResponse:
    return FilingFkMarkResponse.model_validate(saved)


@router.get("", response_model=list[FilingFkMarkResponse])
async def list_filing_fk_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FilingFkMarkResponse]:
    packed = await FilingFkMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=FilingFkMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_filing_fk_mark(
    body: FilingFkMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FilingFkMarkResponse:
    saved = await FilingFkMarkService(session).persist_filing_fk_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        fk_kind=body.fk_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
