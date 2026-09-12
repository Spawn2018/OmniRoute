"""HTTP katalog warunków płatności — HITL, bez kolumny shipment i payment_terms_days."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.payment_terms_mark import PaymentTermsMark
from app.services.payment_terms_marks.payment_terms_mark_service import (
    PaymentTermsMarkService,
)

router = APIRouter(prefix="/payment-terms-marks", tags=["payment-terms-mark"])
_PERM = "can_manage_payment_terms_marks"


class PaymentTermsMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    terms_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class PaymentTermsMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    terms_kind: str
    source_ref: str


def _to_dto(row: PaymentTermsMark) -> PaymentTermsMarkResponse:
    return PaymentTermsMarkResponse.model_validate(row)


@router.get("", response_model=list[PaymentTermsMarkResponse])
async def list_payment_terms_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PaymentTermsMarkResponse]:
    catalog = PaymentTermsMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=PaymentTermsMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment_terms_mark(
    body: PaymentTermsMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PaymentTermsMarkResponse:
    catalog = PaymentTermsMarkService(session)
    saved = await catalog.persist_payment_terms_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        terms_kind=body.terms_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "payment-terms-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
