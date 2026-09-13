"""HTTP otwarty słownik rodzaju wyniku — HITL wiersz, bez CHECK."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.outcome_kind import OutcomeKind
from app.services.outcome_kinds.outcome_kind_service import OutcomeKindService

router = APIRouter(prefix="/outcome-kinds", tags=["outcome-kinds"])
_PERM = "can_manage_outcome_kinds"


class OutcomeKindCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind_code: str = Field(min_length=2, max_length=32)
    source_ref: str = Field(min_length=1, max_length=256)


class OutcomeKindResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    kind_code: str
    source_ref: str


def _as_row(row: OutcomeKind) -> OutcomeKindResponse:
    return OutcomeKindResponse(
        id=row.id,
        organization_id=row.organization_id,
        kind_code=row.kind_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[OutcomeKindResponse])
async def list_outcome_kinds(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OutcomeKindResponse]:
    rows = await OutcomeKindService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=OutcomeKindResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_outcome_kind(
    body: OutcomeKindCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OutcomeKindResponse:
    saved = await OutcomeKindService(session).persist_kind(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        kind_code=body.kind_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "outcome-kind"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
