from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.rank_mark import RankMark
from app.services.rank_marks.rank_mark_service import RankMarkService

router = APIRouter(prefix="/rank-marks", tags=["rank-marks"])

_PERM = "can_manage_rank_marks"


class RankMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rank_kind: str
    source_ref: str


class RankMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    rank_kind: str
    source_ref: str


def _as_row(row: RankMark) -> RankMarkResponse:
    return RankMarkResponse.model_validate(row)


@router.get("", response_model=list[RankMarkResponse])
async def list_rank_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RankMarkResponse]:
    rows = await RankMarkService(session).list_axes()
    return [_as_row(row) for row in rows]


@router.post("", response_model=RankMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_rank_mark(
    body: RankMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RankMarkResponse:
    row = await RankMarkService(session).record_axis(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        rank_kind=body.rank_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
