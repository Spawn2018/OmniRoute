"""HTTP katalog dual ledger — HITL, bez drugiej marży i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.dual_ledger_mark import DualLedgerMark
from app.services.dual_ledger_marks.dual_ledger_mark_service import (
    DualLedgerMarkService,
)

router = APIRouter(prefix="/dual-ledger-marks", tags=["dual-ledger-mark"])
_PERM = "can_manage_dual_ledger_marks"


class DualLedgerMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    ledger_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class DualLedgerMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    ledger_kind: str
    source_ref: str


def _to_dto(row: DualLedgerMark) -> DualLedgerMarkResponse:
    return DualLedgerMarkResponse.model_validate(row)


@router.get("", response_model=list[DualLedgerMarkResponse])
async def list_dual_ledger_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DualLedgerMarkResponse]:
    catalog = DualLedgerMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=DualLedgerMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dual_ledger_mark(
    body: DualLedgerMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DualLedgerMarkResponse:
    catalog = DualLedgerMarkService(session)
    saved = await catalog.persist_dual_ledger_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        ledger_kind=body.ledger_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "dual-ledger-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
