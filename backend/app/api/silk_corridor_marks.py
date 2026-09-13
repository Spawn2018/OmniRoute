from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.silk_corridor_mark import SilkCorridorMark
from app.services.silk_corridor_marks.silk_corridor_mark_service import SilkCorridorMarkService

router = APIRouter(prefix="/silk-corridor-marks", tags=["silk-corridor-marks"])

_PERM = "can_manage_silk_corridor_marks"


class SilkCorridorMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    corridor_kind: str
    source_ref: str


class SilkCorridorMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    corridor_kind: str
    source_ref: str


def _row(saved: SilkCorridorMark) -> SilkCorridorMarkResponse:
    return SilkCorridorMarkResponse.model_validate(saved)


@router.get("", response_model=list[SilkCorridorMarkResponse])
async def list_silk_corridor_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SilkCorridorMarkResponse]:
    packed = await SilkCorridorMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=SilkCorridorMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_silk_corridor_mark(
    body: SilkCorridorMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SilkCorridorMarkResponse:
    saved = await SilkCorridorMarkService(session).persist_silk_corridor_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        corridor_kind=body.corridor_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
