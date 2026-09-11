from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.working_capital_mark import WorkingCapitalMark
from app.services.working_capital_marks.working_capital_mark_service import (
    WorkingCapitalMarkService,
)

router = APIRouter(prefix="/working-capital-marks", tags=["working-capital-marks"])

_PERM = "can_manage_working_capital_marks"


class WorkingCapitalMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    capital_kind: str
    source_ref: str


class WorkingCapitalMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    capital_kind: str
    source_ref: str


def _row(saved: WorkingCapitalMark) -> WorkingCapitalMarkResponse:
    return WorkingCapitalMarkResponse.model_validate(saved)


@router.get("", response_model=list[WorkingCapitalMarkResponse])
async def list_working_capital_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[WorkingCapitalMarkResponse]:
    packed = await WorkingCapitalMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=WorkingCapitalMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_working_capital_mark(
    body: WorkingCapitalMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> WorkingCapitalMarkResponse:
    saved = await WorkingCapitalMarkService(session).persist_working_capital_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        capital_kind=body.capital_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
