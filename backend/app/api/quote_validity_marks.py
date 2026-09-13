"""HTTP katalog quote validity — HITL, bez kolumny quotation i daty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.quote_validity_mark import QuoteValidityMark
from app.services.quote_validity_marks.quote_validity_mark_service import (
    QuoteValidityMarkService,
)

router = APIRouter(prefix="/quote-validity-marks", tags=["quote-validity-mark"])
_PERM = "can_manage_quote_validity_marks"


class QuoteValidityMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    validity_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class QuoteValidityMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    validity_kind: str
    source_ref: str


def _to_dto(row: QuoteValidityMark) -> QuoteValidityMarkResponse:
    return QuoteValidityMarkResponse.model_validate(row)


@router.get("", response_model=list[QuoteValidityMarkResponse])
async def list_quote_validity_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[QuoteValidityMarkResponse]:
    catalog = QuoteValidityMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=QuoteValidityMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_quote_validity_mark(
    body: QuoteValidityMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> QuoteValidityMarkResponse:
    catalog = QuoteValidityMarkService(session)
    saved = await catalog.persist_quote_validity_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        validity_kind=body.validity_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "quote-validity-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
