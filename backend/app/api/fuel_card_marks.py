"""HTTP katalog fuel card — HITL, bez live API i litrów."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.fuel_card_mark import FuelCardMark
from app.services.fuel_card_marks.fuel_card_mark_service import (
    FuelCardMarkService,
)

router = APIRouter(prefix="/fuel-card-marks", tags=["fuel-card-mark"])
_PERM = "can_manage_fuel_card_marks"


class FuelCardMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    card_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class FuelCardMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    card_kind: str
    source_ref: str


def _to_dto(row: FuelCardMark) -> FuelCardMarkResponse:
    return FuelCardMarkResponse.model_validate(row)


@router.get("", response_model=list[FuelCardMarkResponse])
async def list_fuel_card_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FuelCardMarkResponse]:
    catalog = FuelCardMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=FuelCardMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_fuel_card_mark(
    body: FuelCardMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FuelCardMarkResponse:
    catalog = FuelCardMarkService(session)
    saved = await catalog.persist_fuel_card_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        card_kind=body.card_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "fuel-card-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
