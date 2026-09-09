from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_carbon_mark import TenderCarbonMark
from app.services.tender_carbon_marks.tender_carbon_mark_service import (
    TenderCarbonMarkService,
)
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-carbon-marks", tags=["tender-carbon-marks"])

_PERM = "can_manage_tender_carbon_marks"


class TenderCarbonMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    mark_code: str
    source_ref: str


class TenderCarbonMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    mark_code: str
    source_ref: str


def _as_row(row: TenderCarbonMark) -> TenderCarbonMarkResponse:
    return TenderCarbonMarkResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        mark_code=row.mark_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderCarbonMarkResponse])
async def list_tender_carbon_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderCarbonMarkResponse]:
    rows = await TenderCarbonMarkService(session).list_marks()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TenderCarbonMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tender_carbon_mark(
    body: TenderCarbonMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderCarbonMarkResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderCarbonMarkService(session).persist_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        mark_code=body.mark_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
