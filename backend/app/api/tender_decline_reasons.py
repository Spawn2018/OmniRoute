from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_decline_reason import TenderDeclineReason
from app.services.tender_decline_reasons.tender_decline_reason_service import (
    TenderDeclineReasonService,
)

router = APIRouter(prefix="/tender-decline-reasons", tags=["tender-decline-reasons"])

_RELATION = "can_manage_tender_decline_reasons"


class TenderDeclineReasonCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    decline_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class TenderDeclineReasonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    decline_kind: str
    source_ref: str


def _as_response(row: TenderDeclineReason) -> TenderDeclineReasonResponse:
    return TenderDeclineReasonResponse.model_validate(row)


@router.get("", response_model=list[TenderDeclineReasonResponse])
async def list_tender_decline_reasons(
    _authz: None = Depends(require_permission(_RELATION, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderDeclineReasonResponse]:
    service = TenderDeclineReasonService(session)
    return [_as_response(row) for row in await service.list_marks()]


@router.post(
    "",
    response_model=TenderDeclineReasonResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tender_decline_reason(
    body: TenderDeclineReasonCreate,
    _authz: None = Depends(require_permission(_RELATION, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderDeclineReasonResponse:
    service = TenderDeclineReasonService(session)
    saved = await service.persist_tender_decline_reason(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        decline_kind=body.decline_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
