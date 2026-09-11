from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.make_or_buy_mark import MakeOrBuyMark
from app.services.make_or_buy_marks.make_or_buy_mark_service import (
    MakeOrBuyMarkService,
)

router = APIRouter(prefix="/make-or-buy-marks", tags=["make-or-buy-marks"])

_PERM = "can_manage_make_or_buy_marks"


class MakeOrBuyMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    buy_kind: str
    source_ref: str


class MakeOrBuyMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    buy_kind: str
    source_ref: str


def _row(saved: MakeOrBuyMark) -> MakeOrBuyMarkResponse:
    return MakeOrBuyMarkResponse.model_validate(saved)


@router.get("", response_model=list[MakeOrBuyMarkResponse])
async def list_make_or_buy_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MakeOrBuyMarkResponse]:
    packed = await MakeOrBuyMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=MakeOrBuyMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_make_or_buy_mark(
    body: MakeOrBuyMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MakeOrBuyMarkResponse:
    saved = await MakeOrBuyMarkService(session).persist_make_or_buy_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        buy_kind=body.buy_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
