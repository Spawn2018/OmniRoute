"""HTTP otwarty słownik poziomu autonomii — HITL wiersz, bez CHECK."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.autonomy_level import AutonomyLevel
from app.services.autonomy_levels.autonomy_level_service import AutonomyLevelService

router = APIRouter(prefix="/autonomy-levels", tags=["autonomy-levels"])
_PERM = "can_manage_autonomy_levels"


class AutonomyLevelCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level_code: str = Field(min_length=2, max_length=32)
    source_ref: str = Field(min_length=1, max_length=256)


class AutonomyLevelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    level_code: str
    source_ref: str


def _as_row(row: AutonomyLevel) -> AutonomyLevelResponse:
    return AutonomyLevelResponse(
        id=row.id,
        organization_id=row.organization_id,
        level_code=row.level_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[AutonomyLevelResponse])
async def list_autonomy_levels(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AutonomyLevelResponse]:
    rows = await AutonomyLevelService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post("", response_model=AutonomyLevelResponse, status_code=status.HTTP_201_CREATED)
async def create_autonomy_level(
    body: AutonomyLevelCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AutonomyLevelResponse:
    saved = await AutonomyLevelService(session).persist_level(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        level_code=body.level_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "autonomy-level"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
