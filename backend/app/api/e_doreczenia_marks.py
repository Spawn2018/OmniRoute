"""HTTP katalog e-Doręczenia — HITL, bez live ADE i bajtów PDF."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.e_doreczenia_mark import EDoreczeniaMark
from app.services.e_doreczenia_marks.e_doreczenia_mark_service import (
    EDoreczeniaMarkService,
)

router = APIRouter(prefix="/e-doreczenia-marks", tags=["e-doreczenia-mark"])
_PERM = "can_manage_e_doreczenia_marks"


class EDoreczeniaMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    delivery_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class EDoreczeniaMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    delivery_kind: str
    source_ref: str


def _to_dto(row: EDoreczeniaMark) -> EDoreczeniaMarkResponse:
    return EDoreczeniaMarkResponse.model_validate(row)


@router.get("", response_model=list[EDoreczeniaMarkResponse])
async def list_e_doreczenia_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[EDoreczeniaMarkResponse]:
    catalog = EDoreczeniaMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=EDoreczeniaMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_e_doreczenia_mark(
    body: EDoreczeniaMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> EDoreczeniaMarkResponse:
    catalog = EDoreczeniaMarkService(session)
    saved = await catalog.persist_e_doreczenia_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        delivery_kind=body.delivery_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "e-doreczenia-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
