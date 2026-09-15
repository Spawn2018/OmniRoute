"""HTTP otwarty słownik poziomu alokacji — HITL wiersz, bez CHECK 12."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.allocation_level import AllocationLevel
from app.services.allocation_levels.allocation_level_service import AllocationLevelService

router = APIRouter(prefix="/allocation-levels", tags=["allocation-levels"])
_PERM = "can_manage_allocation_levels"


class AllocationLevelCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level_code: str = Field(min_length=2, max_length=32)
    source_ref: str = Field(min_length=1, max_length=256)


class AllocationLevelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    level_code: str
    source_ref: str


def _as_row(row: AllocationLevel) -> AllocationLevelResponse:
    return AllocationLevelResponse(
        id=row.id,
        organization_id=row.organization_id,
        level_code=row.level_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[AllocationLevelResponse])
async def list_allocation_levels(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AllocationLevelResponse]:
    rows = await AllocationLevelService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post("", response_model=AllocationLevelResponse, status_code=status.HTTP_201_CREATED)
async def create_allocation_level(
    body: AllocationLevelCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AllocationLevelResponse:
    saved = await AllocationLevelService(session).persist_level(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        level_code=body.level_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "allocation-level"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
