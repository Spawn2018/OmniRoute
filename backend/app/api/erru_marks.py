"""HTTP katalog sprawdzenia ERRU — HITL, bez live ERRU i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.erru_mark import ErruMark
from app.services.erru_marks.erru_mark_service import ErruMarkService

router = APIRouter(prefix="/erru-marks", tags=["erru-mark"])
_PERM = "can_manage_erru_marks"


class ErruMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    check_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class ErruMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    check_kind: str
    source_ref: str


def _to_dto(row: ErruMark) -> ErruMarkResponse:
    return ErruMarkResponse.model_validate(row)


@router.get("", response_model=list[ErruMarkResponse])
async def list_erru_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ErruMarkResponse]:
    catalog = ErruMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=ErruMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_erru_mark(
    body: ErruMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ErruMarkResponse:
    catalog = ErruMarkService(session)
    saved = await catalog.persist_erru_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        check_kind=body.check_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "erru-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
