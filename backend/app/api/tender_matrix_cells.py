from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_matrix_cell import TenderMatrixCell
from app.services.tender_matrix_cells.tender_matrix_cell_service import TenderMatrixCellService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-matrix-cells", tags=["tender-matrix-cells"])

_PERM = "can_manage_tender_matrix_cells"


class TenderMatrixCellCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    cell_code: str
    amount: str
    currency: str
    source_ref: str


class TenderMatrixCellResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    cell_code: str
    amount: str
    currency: str
    source_ref: str


def _as_row(row: TenderMatrixCell) -> TenderMatrixCellResponse:
    return TenderMatrixCellResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        cell_code=row.cell_code,
        amount=format(row.amount, "f"),
        currency=str(row.currency).strip(),
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderMatrixCellResponse])
async def list_tender_matrix_cells(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderMatrixCellResponse]:
    rows = await TenderMatrixCellService(session).list_cells()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderMatrixCellResponse, status_code=status.HTTP_201_CREATED)
async def create_tender_matrix_cell(
    body: TenderMatrixCellCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderMatrixCellResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderMatrixCellService(session).record_cell(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        cell_code=body.cell_code,
        amount=body.amount,
        currency=body.currency,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
