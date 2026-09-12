"""HTTP katalog miejsca nazwanego — HITL, bez cytatu ICC i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.named_place_mark import NamedPlaceMark
from app.services.named_place_marks.named_place_mark_service import (
    NamedPlaceMarkService,
)

router = APIRouter(prefix="/named-place-marks", tags=["named-place-mark"])
_PERM = "can_manage_named_place_marks"


class NamedPlaceMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    named_place: str = Field(min_length=1, max_length=128)
    terms_version: str = Field(min_length=4, max_length=4)
    source_ref: str = Field(min_length=1, max_length=256)


class NamedPlaceMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    named_place: str
    terms_version: str
    source_ref: str


def _to_dto(row: NamedPlaceMark) -> NamedPlaceMarkResponse:
    return NamedPlaceMarkResponse.model_validate(row)


@router.get("", response_model=list[NamedPlaceMarkResponse])
async def list_named_place_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NamedPlaceMarkResponse]:
    catalog = NamedPlaceMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=NamedPlaceMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_named_place_mark(
    body: NamedPlaceMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NamedPlaceMarkResponse:
    catalog = NamedPlaceMarkService(session)
    saved = await catalog.persist_named_place_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        named_place=body.named_place,
        terms_version=body.terms_version,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "named-place-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
