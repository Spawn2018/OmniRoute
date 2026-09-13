"""HTTP ledger faktu — HITL, bez liczenia błędu przedziału i bez FK do podpowiedzi."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.outcome_ledger import OutcomeLedger
from app.services.outcome_ledgers.outcome_ledger_service import OutcomeLedgerService

router = APIRouter(prefix="/outcome-ledgers", tags=["outcome-ledgers"])
_PERM = "can_manage_outcome_ledgers"


class OutcomeLedgerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_bc: str = Field(min_length=2, max_length=32)
    entity_id: str = Field(min_length=36, max_length=36)
    suggestion_id: str = Field(min_length=36, max_length=36)
    outcome_kind: str = Field(min_length=2, max_length=16)
    actual_value: str
    source_ref: str = Field(min_length=1, max_length=256)


class OutcomeLedgerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    target_bc: str
    entity_id: UUID
    suggestion_id: UUID
    outcome_kind: str
    actual_value: str
    source_ref: str


def _as_row(row: OutcomeLedger) -> OutcomeLedgerResponse:
    return OutcomeLedgerResponse(
        id=row.id,
        organization_id=row.organization_id,
        target_bc=row.target_bc,
        entity_id=row.entity_id,
        suggestion_id=row.suggestion_id,
        outcome_kind=row.outcome_kind,
        actual_value=format(row.actual_value, "f"),
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[OutcomeLedgerResponse])
async def list_outcome_ledgers(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OutcomeLedgerResponse]:
    rows = await OutcomeLedgerService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=OutcomeLedgerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_outcome_ledger(
    body: OutcomeLedgerCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OutcomeLedgerResponse:
    saved = await OutcomeLedgerService(session).persist_ledger(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        target_bc=body.target_bc,
        entity_id=body.entity_id,
        suggestion_id=body.suggestion_id,
        outcome_kind=body.outcome_kind,
        actual_value=body.actual_value,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "outcome-ledger"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
