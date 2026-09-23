from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.margin_match_mark import MarginMatchMark
from app.services.margin_match_marks.margin_match_mark_service import (
    MarginMatchMarkService,
)

router = APIRouter(
    prefix="/margin-match-marks",
    tags=["margin-match-marks"],
)

_PERM = "can_manage_margin_match_marks"


class MarginMatchMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    match_kind: str
    source_ref: str


class MarginMatchMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    match_kind: str
    source_ref: str


def _as_response(row: MarginMatchMark) -> MarginMatchMarkResponse:
    return MarginMatchMarkResponse.model_validate(row)


@router.get("", response_model=list[MarginMatchMarkResponse])
async def list_margin_match_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MarginMatchMarkResponse]:
    rows = await MarginMatchMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=MarginMatchMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_margin_match_mark(
    body: MarginMatchMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MarginMatchMarkResponse:
    saved = await MarginMatchMarkService(session).persist_margin_match_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        match_kind=body.match_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
