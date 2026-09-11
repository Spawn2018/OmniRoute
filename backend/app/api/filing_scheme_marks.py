from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.filing_scheme_mark import FilingSchemeMark
from app.services.filing_scheme_marks.filing_scheme_mark_service import FilingSchemeMarkService

router = APIRouter(prefix="/filing-scheme-marks", tags=["filing-scheme-marks"])

_PERM = "can_manage_filing_scheme_marks"


class FilingSchemeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    scheme_kind: str
    source_ref: str


class FilingSchemeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    scheme_kind: str
    source_ref: str


def _row(saved: FilingSchemeMark) -> FilingSchemeMarkResponse:
    return FilingSchemeMarkResponse.model_validate(saved)


@router.get("", response_model=list[FilingSchemeMarkResponse])
async def list_filing_scheme_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FilingSchemeMarkResponse]:
    packed = await FilingSchemeMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=FilingSchemeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_filing_scheme_mark(
    body: FilingSchemeMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FilingSchemeMarkResponse:
    saved = await FilingSchemeMarkService(session).persist_filing_scheme_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        scheme_kind=body.scheme_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
