"""HTTP katalog protokołu high-value — HITL, bez kolumny shipment i cargo_value."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.high_value_mark import HighValueMark
from app.services.high_value_marks.high_value_mark_service import (
    HighValueMarkService,
)

router = APIRouter(prefix="/high-value-marks", tags=["high-value-mark"])
_PERM = "can_manage_high_value_marks"


class HighValueMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    protocol_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class HighValueMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    protocol_kind: str
    source_ref: str


def _to_dto(row: HighValueMark) -> HighValueMarkResponse:
    return HighValueMarkResponse.model_validate(row)


@router.get("", response_model=list[HighValueMarkResponse])
async def list_high_value_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[HighValueMarkResponse]:
    catalog = HighValueMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=HighValueMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_high_value_mark(
    body: HighValueMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> HighValueMarkResponse:
    catalog = HighValueMarkService(session)
    saved = await catalog.persist_high_value_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        protocol_kind=body.protocol_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "high-value-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
