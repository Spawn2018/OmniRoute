"""HTTP ledger podpowiedzi — HITL, bez zapisu LLM i bez CRPS liczonego."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.suggestion_ledger import SuggestionLedger
from app.services.suggestion_ledgers.suggestion_ledger_service import SuggestionLedgerService

router = APIRouter(prefix="/suggestion-ledgers", tags=["suggestion-ledgers"])
_PERM = "can_manage_suggestion_ledgers"


class SuggestionLedgerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_bc: str = Field(min_length=2, max_length=32)
    entity_id: str = Field(min_length=36, max_length=36)
    suggestion_kind: str = Field(min_length=2, max_length=32)
    interval_low: str
    interval_high: str
    model_version: str = Field(min_length=2, max_length=32)
    prompt_version: str = Field(min_length=2, max_length=32)
    reaction: str = Field(min_length=2, max_length=16)
    changed_to: str = Field(min_length=1, max_length=256)
    source_ref: str = Field(min_length=1, max_length=256)


class SuggestionLedgerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    target_bc: str
    entity_id: UUID
    suggestion_kind: str
    interval_low: str
    interval_high: str
    model_version: str
    prompt_version: str
    reaction: str
    changed_to: str
    source_ref: str


def _as_row(row: SuggestionLedger) -> SuggestionLedgerResponse:
    return SuggestionLedgerResponse(
        id=row.id,
        organization_id=row.organization_id,
        target_bc=row.target_bc,
        entity_id=row.entity_id,
        suggestion_kind=row.suggestion_kind,
        interval_low=format(row.interval_low, "f"),
        interval_high=format(row.interval_high, "f"),
        model_version=row.model_version,
        prompt_version=row.prompt_version,
        reaction=row.reaction,
        changed_to=row.changed_to,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[SuggestionLedgerResponse])
async def list_suggestion_ledgers(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SuggestionLedgerResponse]:
    rows = await SuggestionLedgerService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=SuggestionLedgerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_suggestion_ledger(
    body: SuggestionLedgerCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SuggestionLedgerResponse:
    saved = await SuggestionLedgerService(session).persist_ledger(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        target_bc=body.target_bc,
        entity_id=body.entity_id,
        suggestion_kind=body.suggestion_kind,
        interval_low=body.interval_low,
        interval_high=body.interval_high,
        model_version=body.model_version,
        prompt_version=body.prompt_version,
        reaction=body.reaction,
        changed_to=body.changed_to,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "suggestion-ledger"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
