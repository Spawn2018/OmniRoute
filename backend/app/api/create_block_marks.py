from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.create_block_mark import CreateBlockMark
from app.services.create_block_marks.create_block_mark_service import (
    CreateBlockMarkService,
)

router = APIRouter(
    prefix="/create-block-marks",
    tags=["create-block-marks"],
)

_PERM = "can_manage_create_block_marks"


class CreateBlockMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    block_kind: str
    source_ref: str


class CreateBlockMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    block_kind: str
    source_ref: str


def _row(saved: CreateBlockMark) -> CreateBlockMarkResponse:
    return CreateBlockMarkResponse.model_validate(saved)


@router.get("", response_model=list[CreateBlockMarkResponse])
async def list_create_block_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CreateBlockMarkResponse]:
    packed = await CreateBlockMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CreateBlockMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_create_block_mark(
    body: CreateBlockMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CreateBlockMarkResponse:
    saved = await CreateBlockMarkService(session).persist_create_block_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        block_kind=body.block_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
