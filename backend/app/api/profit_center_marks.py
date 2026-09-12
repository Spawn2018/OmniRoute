"""HTTP katalog centrum zysku/kosztu/projektu — HITL, bez kolumny shipment i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.profit_center_mark import ProfitCenterMark
from app.services.profit_center_marks.profit_center_mark_service import (
    ProfitCenterMarkService,
)

router = APIRouter(prefix="/profit-center-marks", tags=["profit-center-mark"])
_PERM = "can_manage_profit_center_marks"


class ProfitCenterMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    center_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class ProfitCenterMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    center_kind: str
    source_ref: str


def _to_dto(row: ProfitCenterMark) -> ProfitCenterMarkResponse:
    return ProfitCenterMarkResponse.model_validate(row)


@router.get("", response_model=list[ProfitCenterMarkResponse])
async def list_profit_center_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ProfitCenterMarkResponse]:
    catalog = ProfitCenterMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=ProfitCenterMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profit_center_mark(
    body: ProfitCenterMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ProfitCenterMarkResponse:
    catalog = ProfitCenterMarkService(session)
    saved = await catalog.persist_profit_center_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        center_kind=body.center_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "profit-center-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
