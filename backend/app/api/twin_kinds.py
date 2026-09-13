"""HTTP otwarty słownik rodzaju bliźniaka — HITL wiersz, bez CHECK."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.twin_kind import TwinKind
from app.services.twin_kinds.twin_kind_service import TwinKindService

router = APIRouter(prefix="/twin-kinds", tags=["twin-kinds"])
_PERM = "can_manage_twin_kinds"


class TwinKindCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind_code: str = Field(min_length=2, max_length=32)
    source_ref: str = Field(min_length=1, max_length=256)


class TwinKindResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    kind_code: str
    source_ref: str


def _as_row(row: TwinKind) -> TwinKindResponse:
    return TwinKindResponse(
        id=row.id,
        organization_id=row.organization_id,
        kind_code=row.kind_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TwinKindResponse])
async def list_twin_kinds(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TwinKindResponse]:
    rows = await TwinKindService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TwinKindResponse, status_code=status.HTTP_201_CREATED)
async def create_twin_kind(
    body: TwinKindCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TwinKindResponse:
    saved = await TwinKindService(session).persist_kind(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        kind_code=body.kind_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "twin-kind"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
