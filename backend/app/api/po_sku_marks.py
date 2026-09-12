"""HTTP katalog po sku — HITL, bez live EDI i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.po_sku_mark import PoSkuMark
from app.services.po_sku_marks.po_sku_mark_service import (
    PoSkuMarkService,
)

router = APIRouter(prefix="/po-sku-marks", tags=["po-sku-mark"])
_PERM = "can_manage_po_sku_marks"


class PoSkuMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    sku_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class PoSkuMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    sku_kind: str
    source_ref: str


def _to_dto(row: PoSkuMark) -> PoSkuMarkResponse:
    return PoSkuMarkResponse.model_validate(row)


@router.get("", response_model=list[PoSkuMarkResponse])
async def list_po_sku_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PoSkuMarkResponse]:
    catalog = PoSkuMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=PoSkuMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_po_sku_mark(
    body: PoSkuMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PoSkuMarkResponse:
    catalog = PoSkuMarkService(session)
    saved = await catalog.persist_po_sku_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        sku_kind=body.sku_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "po-sku-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
