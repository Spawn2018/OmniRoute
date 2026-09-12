"""HTTP katalog zakazu copy claimów — HITL, bez silnika banów i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.copy_ban_mark import CopyBanMark
from app.services.copy_ban_marks.copy_ban_mark_service import CopyBanMarkService

router = APIRouter(prefix="/copy-ban-marks", tags=["copy-ban"])
_PERM = "can_manage_copy_ban_marks"


class CopyBanMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    ban_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class CopyBanMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    ban_kind: str
    source_ref: str


def _to_dto(row: CopyBanMark) -> CopyBanMarkResponse:
    return CopyBanMarkResponse.model_validate(row)


@router.get("", response_model=list[CopyBanMarkResponse])
async def list_copy_ban_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CopyBanMarkResponse]:
    catalog = CopyBanMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=CopyBanMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_copy_ban_mark(
    body: CopyBanMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CopyBanMarkResponse:
    catalog = CopyBanMarkService(session)
    saved = await catalog.persist_copy_ban_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        ban_kind=body.ban_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "copy-ban-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
