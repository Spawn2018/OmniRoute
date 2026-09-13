"""HTTP otwarty słownik rodzaju podpowiedzi — HITL wiersz, bez CHECK."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.suggestion_kind import SuggestionKind
from app.services.suggestion_kinds.suggestion_kind_service import SuggestionKindService

router = APIRouter(prefix="/suggestion-kinds", tags=["suggestion-kinds"])
_PERM = "can_manage_suggestion_kinds"


class SuggestionKindCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind_code: str = Field(min_length=2, max_length=32)
    source_ref: str = Field(min_length=1, max_length=256)


class SuggestionKindResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    kind_code: str
    source_ref: str


def _as_row(row: SuggestionKind) -> SuggestionKindResponse:
    return SuggestionKindResponse(
        id=row.id,
        organization_id=row.organization_id,
        kind_code=row.kind_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[SuggestionKindResponse])
async def list_suggestion_kinds(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SuggestionKindResponse]:
    rows = await SuggestionKindService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=SuggestionKindResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_suggestion_kind(
    body: SuggestionKindCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SuggestionKindResponse:
    saved = await SuggestionKindService(session).persist_kind(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        kind_code=body.kind_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "suggestion-kind"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
