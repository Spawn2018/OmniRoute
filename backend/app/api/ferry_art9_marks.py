from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ferry_art9_mark import FerryArt9Mark
from app.services.ferry_art9_marks.ferry_art9_mark_service import (
    FerryArt9MarkService,
)

router = APIRouter(prefix="/ferry-art9-marks", tags=["ferry-art9-marks"])

_PERM = "can_manage_ferry_art9_marks"


class FerryArt9MarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    ferry_kind: str
    source_ref: str


class FerryArt9MarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    ferry_kind: str
    source_ref: str


def _row(saved: FerryArt9Mark) -> FerryArt9MarkResponse:
    return FerryArt9MarkResponse.model_validate(saved)


@router.get("", response_model=list[FerryArt9MarkResponse])
async def list_ferry_art9_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FerryArt9MarkResponse]:
    packed = await FerryArt9MarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=FerryArt9MarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ferry_art9_mark(
    body: FerryArt9MarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FerryArt9MarkResponse:
    saved = await FerryArt9MarkService(session).persist_ferry_art9_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        ferry_kind=body.ferry_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
