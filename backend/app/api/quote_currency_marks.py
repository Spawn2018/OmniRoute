"""HTTP katalog quote currency — HITL, bez kolumny quotation i NBP."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.quote_currency_mark import QuoteCurrencyMark
from app.services.quote_currency_marks.quote_currency_mark_service import (
    QuoteCurrencyMarkService,
)

router = APIRouter(prefix="/quote-currency-marks", tags=["quote-currency-mark"])
_PERM = "can_manage_quote_currency_marks"

class QuoteCurrencyMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    currency_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)

class QuoteCurrencyMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    currency_kind: str
    source_ref: str

def _to_dto(row: QuoteCurrencyMark) -> QuoteCurrencyMarkResponse:
    return QuoteCurrencyMarkResponse.model_validate(row)

@router.get("", response_model=list[QuoteCurrencyMarkResponse])
async def list_quote_currency_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[QuoteCurrencyMarkResponse]:
    catalog = QuoteCurrencyMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]

@router.post(
    "",
    response_model=QuoteCurrencyMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_quote_currency_mark(
    body: QuoteCurrencyMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> QuoteCurrencyMarkResponse:
    catalog = QuoteCurrencyMarkService(session)
    saved = await catalog.persist_quote_currency_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        currency_kind=body.currency_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "quote-currency-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
