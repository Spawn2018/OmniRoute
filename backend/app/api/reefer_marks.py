"""HTTP katalog reefer — HITL, bez live filing."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.reefer_mark import ReeferMark
from app.services.reefer_marks.reefer_mark_service import ReeferMarkService

router = APIRouter(prefix="/reefer-marks", tags=["reefer"])

_PERM = "can_manage_reefer_marks"


class ReeferMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    reefer_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class ReeferMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    reefer_kind: str
    source_ref: str


def _to_dto(row: ReeferMark) -> ReeferMarkResponse:
    return ReeferMarkResponse.model_validate(row)


@router.get("", response_model=list[ReeferMarkResponse])
async def list_reefer_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ReeferMarkResponse]:
    catalog = ReeferMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=ReeferMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_reefer_mark(
    body: ReeferMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ReeferMarkResponse:
    catalog = ReeferMarkService(session)
    saved = await catalog.persist_reefer_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        reefer_kind=body.reefer_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "reefer-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
