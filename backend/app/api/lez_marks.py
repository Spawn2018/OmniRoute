"""HTTP katalog reefer — HITL, bez live filing."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.lez_mark import LezMark
from app.services.lez_marks.lez_mark_service import LezMarkService

router = APIRouter(prefix="/lez-marks", tags=["empty-depot"])

_PERM = "can_manage_lez_marks"


class LezMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    lez_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class LezMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    lez_kind: str
    source_ref: str


def _to_dto(row: LezMark) -> LezMarkResponse:
    return LezMarkResponse.model_validate(row)


@router.get("", response_model=list[LezMarkResponse])
async def list_lez_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LezMarkResponse]:
    catalog = LezMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=LezMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_lez_mark(
    body: LezMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LezMarkResponse:
    catalog = LezMarkService(session)
    saved = await catalog.persist_lez_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        lez_kind=body.lez_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "lez-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
