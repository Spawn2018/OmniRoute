from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.company_mark import CompanyMark
from app.services.company_marks.company_mark_service import CompanyMarkService

router = APIRouter(prefix="/company-marks", tags=["company-marks"])

_PERM = "can_manage_company_marks"


class CompanyMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    seat_kind: str
    source_ref: str


class CompanyMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    seat_kind: str
    source_ref: str


def _row(saved: CompanyMark) -> CompanyMarkResponse:
    return CompanyMarkResponse.model_validate(saved)


@router.get("", response_model=list[CompanyMarkResponse])
async def list_company_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CompanyMarkResponse]:
    packed = await CompanyMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CompanyMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_company_mark(
    body: CompanyMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CompanyMarkResponse:
    saved = await CompanyMarkService(session).persist_company_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        seat_kind=body.seat_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
