"""HTTP katalog bid decision — HITL, bez kolumny quotation i auto-award."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.bid_decision_mark import BidDecisionMark
from app.services.bid_decision_marks.bid_decision_mark_service import (
    BidDecisionMarkService,
)

router = APIRouter(prefix="/bid-decision-marks", tags=["bid-decision-mark"])
_PERM = "can_manage_bid_decision_marks"


class BidDecisionMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    decision_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class BidDecisionMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    decision_kind: str
    source_ref: str


def _to_dto(row: BidDecisionMark) -> BidDecisionMarkResponse:
    return BidDecisionMarkResponse.model_validate(row)


@router.get("", response_model=list[BidDecisionMarkResponse])
async def list_bid_decision_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BidDecisionMarkResponse]:
    catalog = BidDecisionMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=BidDecisionMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_bid_decision_mark(
    body: BidDecisionMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BidDecisionMarkResponse:
    catalog = BidDecisionMarkService(session)
    saved = await catalog.persist_bid_decision_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        decision_kind=body.decision_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "bid-decision-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
