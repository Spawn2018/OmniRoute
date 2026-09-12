"""HTTP katalog skutku linii — HITL, bez SQL impact i EBITDA."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.line_impact_mark import LineImpactMark
from app.services.line_impact_marks.line_impact_mark_service import (
    LineImpactMarkService,
)

router = APIRouter(prefix="/line-impact-marks", tags=["line-impact-mark"])
_PERM = "can_manage_line_impact_marks"


class LineImpactMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    impact_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class LineImpactMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    impact_kind: str
    source_ref: str


def _to_dto(row: LineImpactMark) -> LineImpactMarkResponse:
    return LineImpactMarkResponse.model_validate(row)


@router.get("", response_model=list[LineImpactMarkResponse])
async def list_line_impact_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LineImpactMarkResponse]:
    catalog = LineImpactMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=LineImpactMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_line_impact_mark(
    body: LineImpactMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LineImpactMarkResponse:
    catalog = LineImpactMarkService(session)
    saved = await catalog.persist_line_impact_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        impact_kind=body.impact_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "line-impact-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
