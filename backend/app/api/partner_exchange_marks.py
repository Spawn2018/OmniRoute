from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.partner_exchange_mark import PartnerExchangeMark
from app.services.partner_exchange_marks.partner_exchange_mark_service import (
    PartnerExchangeMarkService,
)

router = APIRouter(prefix="/partner-exchange-marks", tags=["partner-exchange-marks"])

_PERM = "can_manage_partner_exchange_marks"


class PartnerExchangeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    exchange_kind: str
    source_ref: str


class PartnerExchangeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    exchange_kind: str
    source_ref: str


def _row(saved: PartnerExchangeMark) -> PartnerExchangeMarkResponse:
    return PartnerExchangeMarkResponse.model_validate(saved)


@router.get("", response_model=list[PartnerExchangeMarkResponse])
async def list_partner_exchange_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PartnerExchangeMarkResponse]:
    packed = await PartnerExchangeMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PartnerExchangeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_partner_exchange_mark(
    body: PartnerExchangeMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PartnerExchangeMarkResponse:
    saved = await PartnerExchangeMarkService(session).persist_partner_exchange_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        exchange_kind=body.exchange_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
